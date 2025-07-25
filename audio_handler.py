"""
AudioRecorder simplificado y corregido para grabación simultánea de micrófono y sistema.
Versión optimizada que soluciona los problemas de overflow y sincronización.
"""
import os
import sys
import time
import logging
import threading
import numpy as np
from datetime import datetime
from pathlib import Path
import queue

# Importaciones de PySide6
from PySide6.QtCore import QThread, Signal

# Importaciones de audio
import sounddevice as sd
from scipy.io import wavfile

# Importaciones opcionales
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

try:
    import lameenc
    LAME_AVAILABLE = True
except ImportError:
    LAME_AVAILABLE = False

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('audio_recorder.log')
    ]
)
logger = logging.getLogger(__name__)

# Importaciones locales
try:
    from utils import send_to_webhook, load_config
except ImportError:
    logger.warning("No se pudo importar módulos locales")
    def send_to_webhook(*args, **kwargs):
        return False, "Webhook no disponible"
    def load_config():
        return {}

class AudioRecorder(QThread):
    """Grabador de audio simplificado y optimizado."""
    
    # Señales
    recording_started = Signal()
    recording_finished = Signal(str)
    error_occurred = Signal(str)
    status_update = Signal(str)
    finished_sending = Signal(bool, str)

    def __init__(self, mic_index=None, sys_index=None, webhook_url=None, chunk_duration=4):
        super().__init__()
        self.mic_index = mic_index
        self.sys_index = sys_index
        self.webhook_url = webhook_url
        self.chunk_duration = max(chunk_duration, 2)  # Mínimo 2 segundos
        
        # Control de grabación
        self._stop = threading.Event()
        self.chunk_counter = 0
        
        # Configuración optimizada
        self.samplerate = 44100
        self.channels = 2
        self.dtype = np.int16
        self.blocksize = 4096  # Buffer grande para evitar overflow
        
        # Buffers de audio
        self.mic_buffer = queue.Queue()
        self.sys_buffer = queue.Queue()
        
        # Directorio temporal
        self.temp_dir = Path(__file__).parent / 'temp_audio'
        self.temp_dir.mkdir(exist_ok=True)
        
        logger.info(f"AudioRecorder inicializado: mic={mic_index}, sys={sys_index}, chunk_duration={chunk_duration}s")

    def run(self):
        """Método principal de grabación."""
        try:
            self.status_update.emit("Iniciando grabación...")
            self.recording_started.emit()
            self._stop.clear()
            
            # Iniciar hilos de grabación
            threads = []
            
            if self.mic_index is not None:
                mic_thread = threading.Thread(target=self._record_microphone, daemon=True)
                threads.append(mic_thread)
                mic_thread.start()
            
            if self.sys_index is not None:
                sys_thread = threading.Thread(target=self._record_system, daemon=True)
                threads.append(sys_thread)
                sys_thread.start()
            
            # Hilo de procesamiento
            process_thread = threading.Thread(target=self._process_chunks, daemon=True)
            process_thread.start()
            threads.append(process_thread)
            
            # Esperar hasta que se detenga
            while not self._stop.is_set():
                time.sleep(0.1)
            
            # Esperar a que terminen los hilos
            for thread in threads:
                if thread.is_alive():
                    thread.join(timeout=2.0)
            
            self.status_update.emit("Grabación finalizada")
            
        except Exception as e:
            logger.error(f"Error en grabación: {e}")
            self.error_occurred.emit(str(e))

    def _record_microphone(self):
        """Graba desde el micrófono."""
        if self.mic_index is None:
            return
            
        try:
            device_info = sd.query_devices(self.mic_index)
            logger.info(f"Grabando micrófono: {device_info['name']}")
            
            def callback(indata, frames, time, status):
                if status:
                    logger.warning(f"Mic status: {status}")
                if not self._stop.is_set():
                    # Convertir a mono si es estéreo
                    if len(indata.shape) > 1 and indata.shape[1] > 1:
                        mono_data = np.mean(indata, axis=1)
                    else:
                        mono_data = indata[:, 0] if len(indata.shape) > 1 else indata
                    self.mic_buffer.put(mono_data.copy())
            
            # Configuraciones para el micrófono (priorizando compatibilidad)
            mic_configs = [
                {'channels': 1, 'dtype': 'float32', 'latency': 'high'},
                {'channels': 2, 'dtype': 'float32', 'latency': 'high'},
                {'channels': 1, 'dtype': 'int16', 'latency': 'high'},
                {'channels': 2, 'dtype': 'int16', 'latency': 'high'}
            ]
            
            success = False
            for config in mic_configs:
                try:
                    max_channels = device_info.get('max_input_channels', 2)
                    channels = min(config['channels'], max_channels)
                    
                    if channels == 0:
                        continue
                    
                    with sd.InputStream(
                        device=self.mic_index,
                        channels=channels,
                        samplerate=self.samplerate,
                        callback=callback,
                        blocksize=self.blocksize,
                        dtype=config['dtype'],
                        latency=config['latency']
                    ):
                        logger.info(f"Micrófono grabando con config: {config}")
                        success = True
                        while not self._stop.is_set():
                            sd.sleep(100)
                        break
                except Exception as e:
                    logger.warning(f"Config micrófono {config} falló: {e}")
                    continue
            
            if not success:
                raise Exception("No se pudo configurar grabación del micrófono")
                    
        except Exception as e:
            logger.error(f"Error grabando micrófono: {e}")
            self.error_occurred.emit(f"Error micrófono: {e}")

    def _record_system(self):
        """Graba el audio del sistema usando loopback."""
        if self.sys_index is None:
            return
            
        try:
            device_info = sd.query_devices(self.sys_index)
            logger.info(f"Grabando sistema: {device_info['name']}")
            
            # Obtener el sample rate nativo del dispositivo
            device_samplerate = int(device_info.get('default_samplerate', 44100))
            logger.info(f"Sample rate del dispositivo: {device_samplerate}Hz")
            
            def callback(indata, frames, time, status):
                if status:
                    logger.warning(f"Sys status: {status}")
                if not self._stop.is_set():
                    # Convertir a mono si es estéreo
                    if len(indata.shape) > 1 and indata.shape[1] > 1:
                        mono_data = np.mean(indata, axis=1)
                    else:
                        mono_data = indata[:, 0] if len(indata.shape) > 1 else indata
                    
                    # Resamplear si es necesario
                    if device_samplerate != self.samplerate:
                        # Resampleo simple (para casos básicos)
                        ratio = self.samplerate / device_samplerate
                        if ratio != 1.0:
                            new_length = int(len(mono_data) * ratio)
                            if new_length > 0:
                                indices = np.linspace(0, len(mono_data) - 1, new_length)
                                mono_data = np.interp(indices, np.arange(len(mono_data)), mono_data)
                    
                    self.sys_buffer.put(mono_data.copy())
            
            # Configuraciones con sample rates múltiples
            sample_rates = [device_samplerate, 44100, 48000, 22050]
            configs = []
            
            for sr in sample_rates:
                configs.extend([
                    {'channels': 2, 'dtype': 'float32', 'latency': 'high', 'samplerate': sr},
                    {'channels': 1, 'dtype': 'float32', 'latency': 'high', 'samplerate': sr},
                    {'channels': 2, 'dtype': 'int16', 'latency': 'high', 'samplerate': sr},
                    {'channels': 1, 'dtype': 'int16', 'latency': 'high', 'samplerate': sr}
                ])
            
            success = False
            for config in configs:
                try:
                    # Verificar si el dispositivo tiene canales de entrada
                    max_input_channels = device_info.get('max_input_channels', 0)
                    if max_input_channels == 0:
                        # Si no tiene canales de entrada, intentar como dispositivo de salida con loopback
                        max_channels = device_info.get('max_output_channels', 2)
                    else:
                        max_channels = max_input_channels
                    
                    channels = min(config['channels'], max_channels)
                    if channels == 0:
                        continue
                    
                    with sd.InputStream(
                        device=self.sys_index,
                        channels=channels,
                        samplerate=config['samplerate'],
                        callback=callback,
                        blocksize=self.blocksize,
                        dtype=config['dtype'],
                        latency=config['latency']
                    ):
                        logger.info(f"Sistema grabando con config: {config}")
                        success = True
                        while not self._stop.is_set():
                            sd.sleep(100)
                        break
                except Exception as e:
                    logger.warning(f"Config {config} falló: {e}")
                    continue
            
            if not success:
                raise Exception("No se pudo configurar grabación del sistema")
                
        except Exception as e:
            logger.error(f"Error grabando sistema: {e}")
            self.error_occurred.emit(f"Error sistema: {e}")

    def _process_chunks(self):
        """Procesa y mezcla chunks de audio."""
        chunk_samples = int(self.samplerate * self.chunk_duration)
        mic_data = []
        sys_data = []
        
        # Determinar qué fuentes están activas
        mic_active = self.mic_index is not None
        sys_active = self.sys_index is not None
        
        while not self._stop.is_set():
            try:
                # Recopilar datos del micrófono solo si está activo
                if mic_active:
                    while len(mic_data) < chunk_samples and not self._stop.is_set():
                        try:
                            data = self.mic_buffer.get(timeout=0.1)
                            mic_data.extend(data)
                        except queue.Empty:
                            break
                
                # Recopilar datos del sistema solo si está activo
                if sys_active:
                    while len(sys_data) < chunk_samples and not self._stop.is_set():
                        try:
                            data = self.sys_buffer.get(timeout=0.1)
                            sys_data.extend(data)
                        except queue.Empty:
                            break
                
                # Determinar si tenemos suficientes datos para procesar
                mic_ready = not mic_active or len(mic_data) >= chunk_samples
                sys_ready = not sys_active or len(sys_data) >= chunk_samples
                
                if mic_ready and sys_ready:
                    # Procesar chunk con los datos disponibles
                    mic_chunk = mic_data[:chunk_samples] if mic_active else []
                    sys_chunk = sys_data[:chunk_samples] if sys_active else []
                    
                    self._save_chunk(mic_chunk, sys_chunk)
                    
                    # Remover datos procesados
                    if mic_active:
                        mic_data = mic_data[chunk_samples:]
                    if sys_active:
                        sys_data = sys_data[chunk_samples:]
                    
                    self.chunk_counter += 1
                
            except Exception as e:
                logger.error(f"Error procesando chunk: {e}")
                time.sleep(0.1)
        
        # IMPORTANTE: Procesar el chunk final cuando se detiene la grabación
        # Esto soluciona el problema de que el último audio no se envía
        try:
            # Recopilar cualquier dato restante en los buffers
            while not self.mic_buffer.empty():
                try:
                    data = self.mic_buffer.get_nowait()
                    mic_data.extend(data)
                except queue.Empty:
                    break
            
            while not self.sys_buffer.empty():
                try:
                    data = self.sys_buffer.get_nowait()
                    sys_data.extend(data)
                except queue.Empty:
                    break
            
            # Si hay datos restantes, procesarlos como chunk final
            if mic_data or sys_data:
                logger.info(f"Procesando chunk final con {len(mic_data)} muestras de mic y {len(sys_data)} muestras de sistema")
                self._save_chunk(mic_data, sys_data, is_final=True)
                self.chunk_counter += 1
                
        except Exception as e:
            logger.error(f"Error procesando chunk final: {e}")

    def _save_chunk(self, mic_data, sys_data, is_final=False):
        """Guarda un chunk mezclado."""
        try:
            chunk_id = f"chunk_{self.chunk_counter:04d}"
            if is_final:
                chunk_id += "_FINAL"
                self.status_update.emit(f"Procesando {chunk_id} (último chunk)...")
            else:
                self.status_update.emit(f"Procesando {chunk_id}...")
            
            # Asegurar que ambos arrays tengan la misma longitud
            max_len = max(len(mic_data) if mic_data else 0, len(sys_data) if sys_data else 0)
            if max_len == 0:
                logger.warning("No hay datos de audio para procesar en el chunk")
                return
            
            # Rellenar con ceros si es necesario
            if mic_data and len(mic_data) < max_len:
                mic_data.extend([0] * (max_len - len(mic_data)))
            elif not mic_data:
                mic_data = [0] * max_len
                
            if sys_data and len(sys_data) < max_len:
                sys_data.extend([0] * (max_len - len(sys_data)))
            elif not sys_data:
                sys_data = [0] * max_len
            
            # Convertir a numpy arrays
            mic_array = np.array(mic_data, dtype=np.float32)
            sys_array = np.array(sys_data, dtype=np.float32)
            
            # Determinar qué fuentes están activas
            mic_active = self.mic_index is not None
            sys_active = self.sys_index is not None
            
            # Mezclar audio según las fuentes activas
            if mic_active and sys_active:
                # Ambas fuentes: mezclar con pesos
                mixed = (mic_array * 0.7 + sys_array * 0.5)
            elif mic_active:
                # Solo micrófono
                mixed = mic_array
            elif sys_active:
                # Solo sistema
                mixed = sys_array
            else:
                # No debería llegar aquí, pero por seguridad
                mixed = np.zeros_like(mic_array)
            
            # Normalizar para evitar clipping
            max_val = np.max(np.abs(mixed))
            if max_val > 0:
                mixed = mixed / max_val * 0.8  # Dejar margen del 20%
            
            # Crear directorio para el chunk
            chunk_dir = self.temp_dir / f"chunk_{self.chunk_counter}"
            chunk_dir.mkdir(exist_ok=True)
            
            # Guardar como WAV primero
            wav_path = chunk_dir / f"final_{self.chunk_counter:04d}.wav"
            wavfile.write(str(wav_path), self.samplerate, (mixed * 32767).astype(np.int16))
            
            # Convertir a MP3 si es posible
            mp3_path = chunk_dir / f"final_{self.chunk_counter:04d}.mp3"
            if self._convert_to_mp3(wav_path, mp3_path):
                final_path = mp3_path
                wav_path.unlink()  # Eliminar WAV temporal
            else:
                final_path = wav_path
            
            # Enviar chunk
            if self.webhook_url:
                threading.Thread(
                    target=self._send_chunk,
                    args=(chunk_id, str(final_path), is_final),
                    daemon=True
                ).start()
            
            logger.info(f"Chunk {chunk_id} guardado: {final_path}")
            
        except Exception as e:
            logger.error(f"Error guardando chunk: {e}")
            self.error_occurred.emit(f"Error guardando chunk: {e}")

    def _convert_to_mp3(self, wav_path, mp3_path):
        """Convierte WAV a MP3."""
        try:
            if PYDUB_AVAILABLE:
                audio = AudioSegment.from_wav(str(wav_path))
                audio = audio.set_channels(1)  # Mono
                audio.export(str(mp3_path), format="mp3", bitrate="128k")
                return True
            else:
                logger.warning("pydub no disponible, manteniendo WAV")
                return False
        except Exception as e:
            logger.error(f"Error convirtiendo a MP3: {e}")
            return False

    def _send_chunk(self, chunk_id, file_path, is_final=False):
        """Envía un chunk al webhook."""
        try:
            if not os.path.exists(file_path):
                logger.error(f"Archivo no encontrado: {file_path}")
                return
                
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            if is_final:
                self.status_update.emit(f"Enviando {chunk_id} (ÚLTIMO CHUNK - {file_size:.2f} MB)...")
            else:
                self.status_update.emit(f"Enviando {chunk_id} ({file_size:.2f} MB)...")
            
            # Pasar el parámetro is_final al webhook
            success, message = send_to_webhook(self.webhook_url, file_path, is_final)
            
            self.finished_sending.emit(success, chunk_id)
            
            if success:
                if is_final:
                    self.status_update.emit(f"✅ Enviado {chunk_id} exitosamente (GRABACIÓN COMPLETA)")
                else:
                    self.status_update.emit(f"Enviado {chunk_id} exitosamente")
                # Limpiar archivo después de enviar
                try:
                    os.remove(file_path)
                    # Limpiar directorio si está vacío
                    chunk_dir = Path(file_path).parent
                    if chunk_dir.exists() and not any(chunk_dir.iterdir()):
                        chunk_dir.rmdir()
                except Exception as e:
                    logger.warning(f"Error limpiando archivos: {e}")
            else:
                self.status_update.emit(f"Error enviando {chunk_id}: {message}")
                
        except Exception as e:
            logger.error(f"Error enviando chunk: {e}")
            self.error_occurred.emit(f"Error enviando chunk: {e}")

    def stop_recording(self):
        """Detiene la grabación."""
        self._stop.set()
        self.status_update.emit("Deteniendo grabación...")
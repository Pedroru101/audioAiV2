"""
Audio Capture Widget – Versión Corregida
Ventana flotante con panel de configuración y prueba de dispositivos mejorada.
"""
import sys
import os
import time
import tempfile
from pathlib import Path
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QSize, QThread, Signal as QtSignal
from PySide6.QtGui import QIcon, QPainter, QColor, QPen, QPainterPath, QFont
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QComboBox,
    QLineEdit, QSpinBox, QLabel, QFrame, QProgressBar, QSizePolicy, QSpacerItem, QCheckBox
)

# Importaciones locales
from audio_handler import AudioRecorder
from audio_device_tester import AudioDeviceTester, get_audio_devices
from utils import load_config, save_config

# Importaciones de audio
import sounddevice as sd
import numpy as np
from scipy.io import wavfile

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
STYLE_PATH = os.path.join(ASSETS, "styles", "style.qss")

class DeviceTestThread(QThread):
    """Hilo para probar dispositivos de audio con grabación de 3 segundos."""
    test_completed = QtSignal(dict)
    test_progress = QtSignal(str)
    test_error = QtSignal(str)
    
    def __init__(self, device_id, device_info, test_type, parent=None):
        super().__init__(parent)
        self.device_id = device_id
        self.device_info = device_info
        self.test_type = test_type
        self.should_stop = False
        
    def run(self):
        try:
            if self.test_type == 'input':
                self._test_input_device()
            else:
                self._test_output_device()
        except Exception as e:
            self.test_error.emit(f"Error en la prueba: {str(e)}")
    
    def _test_input_device(self):
        """Prueba un dispositivo de entrada grabando 3 segundos."""
        try:
            self.test_progress.emit("Iniciando prueba de micrófono...")
            
            device_info = sd.query_devices(self.device_id)
            samplerate = int(device_info.get('default_samplerate', 44100))
            channels = min(device_info.get('max_input_channels', 1), 2)
            
            if channels == 0:
                self.test_completed.emit({
                    'status': 'error',
                    'message': 'No tiene canales de entrada',
                    'audio_file': None
                })
                return
            
            self.test_progress.emit("Grabando 3 segundos... ¡Habla al micrófono!")
            
            # Grabar 3 segundos
            duration = 3.0
            recording = sd.rec(
                int(duration * samplerate),
                samplerate=samplerate,
                channels=channels,
                device=self.device_id,
                dtype='float32'
            )
            sd.wait()
            
            if self.should_stop:
                return
            
            # Analizar la grabación
            max_level = np.max(np.abs(recording))
            avg_level = np.mean(np.abs(recording))
            
            # Guardar archivo temporal
            temp_file = None
            if max_level > 0.001:  # Si hay audio significativo
                temp_dir = Path(tempfile.gettempdir()) / "audio_test"
                temp_dir.mkdir(exist_ok=True)
                temp_file = temp_dir / f"test_mic_{self.device_id}_{int(time.time())}.wav"
                
                # Convertir a mono si es estéreo
                if len(recording.shape) > 1 and recording.shape[1] > 1:
                    recording_mono = np.mean(recording, axis=1)
                else:
                    recording_mono = recording[:, 0] if len(recording.shape) > 1 else recording
                
                # Guardar como WAV
                wavfile.write(str(temp_file), samplerate, (recording_mono * 32767).astype(np.int16))
            
            # Determinar resultado
            if max_level > 0.01:
                status = 'success'
                message = f"✅ Funciona correctamente (Nivel: {max_level:.3f})"
            elif max_level > 0.001:
                status = 'warning'
                message = f"⚠️ Audio muy bajo (Nivel: {max_level:.3f})"
            else:
                status = 'error'
                message = "❌ No se detectó audio"
            
            self.test_completed.emit({
                'status': status,
                'message': message,
                'audio_file': str(temp_file) if temp_file else None,
                'max_level': float(max_level),
                'avg_level': float(avg_level)
            })
            
        except Exception as e:
            self.test_error.emit(f"Error probando micrófono: {str(e)}")
    
    def _test_output_device(self):
        """Prueba un dispositivo de sistema grabando audio (loopback)."""
        try:
            self.test_progress.emit("Probando captura de audio del sistema...")
            
            device_info = sd.query_devices(self.device_id)
            
            # SIEMPRE intentar la grabación, sin verificar max_input_channels primero
            # Algunos dispositivos reportan 0 canales pero funcionan para loopback
            self._test_loopback_device()
                
        except Exception as e:
            self.test_error.emit(f"Error probando sistema: {str(e)}")
    
    def _test_loopback_device(self):
        """Prueba un dispositivo probando múltiples configuraciones hasta encontrar una que funcione."""
        try:
            device_info = sd.query_devices(self.device_id)
            device_name = device_info.get('name', 'Unknown')
            
            self.test_progress.emit("Probando configuraciones para captura de sistema...")
            
            # Verificar que el dispositivo tenga canales de entrada
            if device_info['max_input_channels'] == 0:
                raise Exception("El dispositivo no tiene canales de entrada disponibles")
            
            # Configuraciones a probar (basadas en nuestros tests exitosos)
            configs_to_try = [
                # Configuración que funcionó en test_output_only.py
                {'channels': 2, 'dtype': 'float32', 'samplerate': int(device_info.get('default_samplerate', 44100))},
                # Configuraciones alternativas
                {'channels': 1, 'dtype': 'float32', 'samplerate': int(device_info.get('default_samplerate', 44100))},
                {'channels': 2, 'dtype': 'float32', 'samplerate': 44100},
                {'channels': 1, 'dtype': 'float32', 'samplerate': 44100},
                # Si el dispositivo tiene más canales disponibles
                {'channels': min(device_info['max_input_channels'], 2), 'dtype': 'float32', 'samplerate': 44100},
            ]
            
            duration = 3.0  # 3 segundos para el test
            
            for i, config in enumerate(configs_to_try):
                if self.should_stop:
                    return
                
                self.test_progress.emit(f"Probando configuración {i+1}/{len(configs_to_try)}: {config['channels']} canales, {config['samplerate']}Hz")
                
                try:
                    # Usar InputStream como en el test exitoso
                    with sd.InputStream(
                        device=self.device_id,
                        channels=config['channels'],
                        samplerate=config['samplerate'],
                        dtype=config['dtype']
                    ) as stream:
                        
                        self.test_progress.emit("✅ Stream abierto exitosamente, grabando...")
                        
                        # Grabar por segundos para mostrar progreso
                        all_frames = []
                        for segundo in range(int(duration)):
                            data, overflowed = stream.read(config['samplerate'])  # 1 segundo
                            all_frames.append(data)
                            
                            # Análisis en tiempo real
                            max_level = np.max(np.abs(data))
                            self.test_progress.emit(f"Segundo {segundo+1}: Nivel {max_level:.4f}")
                            
                            if self.should_stop:
                                return
                        
                        # Combinar todos los frames
                        audio_data = np.concatenate(all_frames, axis=0)
                    
                    # Analizar resultado usando los mismos umbrales del test exitoso
                    max_level = np.max(np.abs(audio_data))
                    avg_level = np.mean(np.abs(audio_data))
                    
                    self.test_progress.emit(f"Análisis: Nivel máximo {max_level:.6f}")
                    
                    # Usar los mismos umbrales del test exitoso
                    if max_level > 0.1:
                        content_type = "EXCELENTE"
                        status = 'success'
                    elif max_level > 0.01:
                        content_type = "BUENA"
                        status = 'success'
                    elif max_level > 0.001:
                        content_type = "BAJA"
                        status = 'warning'
                    else:
                        content_type = "SIN AUDIO"
                        status = 'error'
                    
                    # Si encontramos audio o es la última configuración, reportar resultado
                    if status in ['success', 'warning'] or i == len(configs_to_try) - 1:
                        
                        if status in ['success', 'warning']:
                            # Guardar archivo temporal
                            temp_dir = Path(tempfile.gettempdir()) / "audio_test"
                            temp_dir.mkdir(exist_ok=True)
                            temp_file = temp_dir / f"test_sys_{self.device_id}_{int(time.time())}.wav"
                            
                            # Guardar como en el test exitoso
                            import wave
                            with wave.open(str(temp_file), 'wb') as wf:
                                wf.setnchannels(config['channels'])
                                wf.setsampwidth(2)  # 16-bit
                                wf.setframerate(config['samplerate'])
                                
                                # Convertir a int16
                                audio_int16 = (audio_data * 32767).astype(np.int16)
                                wf.writeframes(audio_int16.tobytes())
                            
                            message = f"✅ CALIDAD {content_type} - Config: {config['channels']}ch, {config['samplerate']}Hz (Nivel: {max_level:.4f})"
                            
                            self.test_completed.emit({
                                'status': status,
                                'message': message,
                                'audio_file': str(temp_file),
                                'max_level': float(max_level)
                            })
                        else:
                            # No hay audio en ninguna configuración
                            self.test_completed.emit({
                                'status': 'error',
                                'message': f"❌ {content_type} en todas las configuraciones - ¿Está reproduciendo audio?",
                                'audio_file': None
                            })
                        
                        return  # Salir después de encontrar una configuración que funcione o probar todas
                        
                except Exception as config_error:
                    # Esta configuración falló, probar la siguiente
                    self.test_progress.emit(f"❌ Configuración {i+1} falló: {str(config_error)}")
                    continue
            
            # Si llegamos aquí, ninguna configuración funcionó
            self.test_completed.emit({
                'status': 'error',
                'message': "❌ Ninguna configuración funcionó - Verificar dispositivo VB-Audio",
                'audio_file': None
            })
            
        except Exception as e:
            self.test_error.emit(f"Error en loopback: {str(e)}")
    
    def _test_playback_device(self):
        """Prueba un dispositivo de salida reproduciendo un tono."""
        try:
            device_info = sd.query_devices(self.device_id)
            samplerate = int(device_info.get('default_samplerate', 44100))
            channels = min(device_info.get('max_output_channels', 2), 2)
            
            if channels == 0:
                self.test_completed.emit({
                    'status': 'error',
                    'message': 'No tiene canales de salida',
                    'audio_file': None
                })
                return
            
            self.test_progress.emit("Reproduciendo tono de prueba...")
            
            # Generar tono de 440Hz por 1 segundo
            duration = 1.0
            t = np.linspace(0, duration, int(samplerate * duration), False)
            tone = np.sin(2 * np.pi * 440 * t) * 0.3
            
            if channels == 2:
                tone = np.column_stack((tone, tone))
            
            # Reproducir tono
            sd.play(tone, samplerate=samplerate, device=self.device_id)
            sd.wait()
            
            self.test_completed.emit({
                'status': 'success',
                'message': '✅ Tono reproducido correctamente',
                'audio_file': None
            })
            
        except Exception as e:
            self.test_error.emit(f"Error en reproducción: {str(e)}")
    
    def stop(self):
        self.should_stop = True
        self.quit()
        self.wait(1000)

class ConfigPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ConfigPanel")
        self.parent = parent
        
        # Variables para el testeo de dispositivos
        self.device_test_thread = None
        self.current_test = None
        self.current_audio_file = None
        
        self.setMaximumHeight(600)
        self.setMinimumHeight(0)
        self.setContentsMargins(12, 8, 12, 8)

        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Sección de dispositivos de entrada
        input_layout = QVBoxLayout()
        input_layout.setSpacing(4)
        input_label = QLabel("🎤 Micrófono:")
        input_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        input_layout.addWidget(input_label)
        
        input_hbox = QHBoxLayout()
        self.input_combo = QComboBox()
        self.input_combo.setMinimumWidth(200)
        
        # Botones para micrófono
        input_buttons = QHBoxLayout()
        self.test_input_btn = QPushButton("Probar")
        self.test_input_btn.setFixedWidth(60)
        self.test_input_btn.setEnabled(False)
        self.test_input_btn.clicked.connect(lambda: self.test_device('input'))
        
        self.play_input_btn = QPushButton("▶")
        self.play_input_btn.setFixedWidth(30)
        self.play_input_btn.setEnabled(False)
        self.play_input_btn.clicked.connect(lambda: self.play_test_audio('input'))
        self.play_input_btn.setToolTip("Reproducir grabación de prueba")
        
        input_buttons.addWidget(self.test_input_btn)
        input_buttons.addWidget(self.play_input_btn)
        
        input_hbox.addWidget(self.input_combo)
        input_hbox.addLayout(input_buttons)
        input_layout.addLayout(input_hbox)
        
        self.input_status = QLabel("")
        self.input_status.setStyleSheet("font-size: 10px; color: #888; margin-left: 5px;")
        self.input_status.setWordWrap(True)
        input_layout.addWidget(self.input_status)
        
        # Sección de dispositivos de salida (loopback)
        output_layout = QVBoxLayout()
        output_layout.setSpacing(4)
        output_label = QLabel("🔊 Captura de Audio del Sistema:")
        output_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        output_layout.addWidget(output_label)
        
        output_hbox = QHBoxLayout()
        self.output_combo = QComboBox()
        self.output_combo.setMinimumWidth(200)
        
        # Botones para sistema
        output_buttons = QHBoxLayout()
        self.test_output_btn = QPushButton("Probar")
        self.test_output_btn.setFixedWidth(60)
        self.test_output_btn.setEnabled(False)
        self.test_output_btn.clicked.connect(lambda: self.test_device('output'))
        
        self.play_output_btn = QPushButton("▶")
        self.play_output_btn.setFixedWidth(30)
        self.play_output_btn.setEnabled(False)
        self.play_output_btn.clicked.connect(lambda: self.play_test_audio('output'))
        self.play_output_btn.setToolTip("Reproducir audio capturado del sistema")
        
        output_buttons.addWidget(self.test_output_btn)
        output_buttons.addWidget(self.play_output_btn)
        
        output_hbox.addWidget(self.output_combo)
        output_hbox.addLayout(output_buttons)
        output_layout.addLayout(output_hbox)
        
        self.output_status = QLabel("")
        self.output_status.setStyleSheet("font-size: 10px; color: #888; margin-left: 5px;")
        self.output_status.setWordWrap(True)
        output_layout.addWidget(self.output_status)
        
        # Barra de progreso para pruebas
        self.test_progress = QProgressBar()
        self.test_progress.setTextVisible(False)
        self.test_progress.setRange(0, 0)
        self.test_progress.hide()
        
        # Sección de selección de fuentes de grabación
        sources_layout = QVBoxLayout()
        sources_layout.setSpacing(4)
        sources_label = QLabel("🎯 Fuentes de Grabación:")
        sources_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        sources_layout.addWidget(sources_label)
        
        # Checkboxes para seleccionar fuentes
        sources_checkboxes = QHBoxLayout()
        
        self.record_mic_checkbox = QCheckBox("🎤 Grabar Micrófono")
        self.record_mic_checkbox.setChecked(True)  # Por defecto activado
        self.record_mic_checkbox.setStyleSheet("font-size: 11px; padding: 4px;")
        
        self.record_system_checkbox = QCheckBox("🔊 Grabar Sistema")
        self.record_system_checkbox.setChecked(True)  # Por defecto activado
        self.record_system_checkbox.setStyleSheet("font-size: 11px; padding: 4px;")
        
        # Conectar señales para validación
        self.record_mic_checkbox.stateChanged.connect(self.validate_recording_sources)
        self.record_system_checkbox.stateChanged.connect(self.validate_recording_sources)
        
        sources_checkboxes.addWidget(self.record_mic_checkbox)
        sources_checkboxes.addWidget(self.record_system_checkbox)
        sources_checkboxes.addStretch()
        
        sources_layout.addLayout(sources_checkboxes)
        
        # Etiqueta de estado de fuentes
        self.sources_status = QLabel("✅ Grabará: Micrófono + Sistema")
        self.sources_status.setStyleSheet("font-size: 10px; color: #4CAF50; margin-left: 5px;")
        sources_layout.addWidget(self.sources_status)
        
        # Sección de configuración webhook
        webhook_layout = QVBoxLayout()
        webhook_layout.setSpacing(4)
        webhook_label = QLabel("🌐 URL del Webhook (n8n):")
        webhook_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        webhook_layout.addWidget(webhook_label)
        
        self.webhook_edit = QLineEdit()
        self.webhook_edit.setPlaceholderText("http://localhost:5678/webhook-test/audio.ai")
        webhook_layout.addWidget(self.webhook_edit)
        
        # Duración de chunk
        duration_layout = QHBoxLayout()
        duration_label = QLabel("⏱️ Duración chunk (segundos):")
        duration_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(2, 300)
        self.duration_spin.setSuffix(" seg")
        self.duration_spin.setValue(4)
        duration_layout.addWidget(duration_label)
        duration_layout.addWidget(self.duration_spin)
        duration_layout.addStretch()
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        
        # Botón de guardar
        self.save_btn = QPushButton("💾 Guardar Configuración")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        # Botón de cerrar aplicación
        self.close_btn = QPushButton("❌ Cerrar Aplicación")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.close_btn)
        
        # Agregar todo al layout principal
        layout.addLayout(input_layout)
        layout.addLayout(output_layout)
        layout.addWidget(self.test_progress)
        layout.addSpacing(10)
        layout.addLayout(sources_layout)
        layout.addSpacing(5)
        layout.addLayout(webhook_layout)
        layout.addSpacing(5)
        layout.addLayout(duration_layout)
        layout.addStretch()
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
        # Variables para archivos de audio de prueba
        self.input_audio_file = None
        self.output_audio_file = None
        
        # Cargar dispositivos y configuración
        self.load_audio_devices()
        self.load_from_config(load_config())
        
        # Conectar señales
        self.save_btn.clicked.connect(self.save_to_config)
        
        # Validar fuentes iniciales
        self.validate_recording_sources()
    
    def load_audio_devices(self):
        """Carga los dispositivos de audio disponibles con lógica especial para VB-Audio."""
        self.input_combo.clear()
        self.output_combo.clear()
        
        try:
            devices = get_audio_devices()
            input_devices = []  # Para micrófonos reales
            output_devices = []  # Para captura de sistema (VB-Audio Output)
            
            for dev in devices:
                device_name = dev['name'].lower()
                
                # Lógica especial para VB-Audio
                if 'vb-audio' in device_name or 'cable' in device_name:
                    if 'output' in device_name:
                        # CABLE Output = Para capturar sistema
                        if dev['max_input_channels'] > 0:  # Verificar que pueda capturar
                            output_devices.append((dev['id'], dev['name'], dev))
                    # CABLE Input = Para reproducir (no lo agregamos a ninguna lista)
                else:
                    # Dispositivos normales (no VB-Audio)
                    if 'input' in dev['type'] and dev['max_input_channels'] > 0:
                        # Micrófonos reales
                        input_devices.append((dev['id'], dev['name'], dev))
            
            # Ordenar por nombre
            input_devices.sort(key=lambda x: x[1].lower())
            output_devices.sort(key=lambda x: x[1].lower())
            
            # Llenar combo de entrada (micrófonos reales)
            for dev_id, name, dev_info in input_devices:
                display_name = f"{name} ({dev_info['hostapi']})"
                self.input_combo.addItem(display_name, (dev_id, dev_info))
            
            # Llenar combo de salida (captura de sistema - VB-Audio Output)
            for dev_id, name, dev_info in output_devices:
                display_name = f"{name} ({dev_info['hostapi']})"
                self.output_combo.addItem(display_name, (dev_id, dev_info))
            
            # Habilitar botones de prueba
            self.test_input_btn.setEnabled(self.input_combo.count() > 0)
            self.test_output_btn.setEnabled(self.output_combo.count() > 0)
            
            print(f"✅ Dispositivos cargados:")
            print(f"   Micrófonos: {len(input_devices)}")
            print(f"   Captura sistema: {len(output_devices)}")
            
        except Exception as e:
            print(f"Error al cargar dispositivos: {e}")
    
    def load_from_config(self, config):
        """Carga la configuración guardada."""
        # Establecer dispositivos
        if 'input_device' in config and config['input_device'] is not None:
            for i in range(self.input_combo.count()):
                dev_id, dev_info = self.input_combo.itemData(i)
                if dev_id == config['input_device']:
                    self.input_combo.setCurrentIndex(i)
                    break
                    
        if 'output_device' in config and config['output_device'] is not None:
            for i in range(self.output_combo.count()):
                dev_id, dev_info = self.output_combo.itemData(i)
                if dev_id == config['output_device']:
                    self.output_combo.setCurrentIndex(i)
                    break
                    
        if 'webhook_url' in config:
            self.webhook_edit.setText(config['webhook_url'])
            
        if 'chunk_duration' in config:
            self.duration_spin.setValue(config.get('chunk_duration', 4))
            
        # Cargar configuración de fuentes de grabación
        if 'record_microphone' in config:
            self.record_mic_checkbox.setChecked(config['record_microphone'])
        if 'record_system' in config:
            self.record_system_checkbox.setChecked(config['record_system'])
            
        # Validar fuentes después de cargar
        self.validate_recording_sources()
    
    def save_to_config(self):
        """Guarda la configuración actual."""
        input_dev_id = None
        if self.input_combo.currentIndex() >= 0:
            input_dev_id, _ = self.input_combo.currentData()
            
        output_dev_id = None
        if self.output_combo.currentIndex() >= 0:
            output_dev_id, _ = self.output_combo.currentData()
        
        config = {
            'input_device': input_dev_id,
            'output_device': output_dev_id,
            'webhook_url': self.webhook_edit.text().strip(),
            'chunk_duration': self.duration_spin.value()
        }
        
        # Agregar configuración de fuentes de grabación
        config['record_microphone'] = self.record_mic_checkbox.isChecked()
        config['record_system'] = self.record_system_checkbox.isChecked()
        
        save_config(config)
        
        # Mostrar mensaje de confirmación
        if hasattr(self.parent, 'show_status'):
            self.parent.show_status("✅ Configuración guardada", error=False)
        
        return config
    
    def validate_recording_sources(self):
        """Valida que al menos una fuente de grabación esté seleccionada."""
        mic_enabled = self.record_mic_checkbox.isChecked()
        system_enabled = self.record_system_checkbox.isChecked()
        
        if not mic_enabled and not system_enabled:
            # Si ninguna está seleccionada, forzar al menos el micrófono
            self.record_mic_checkbox.setChecked(True)
            mic_enabled = True
        
        # Actualizar etiqueta de estado
        if mic_enabled and system_enabled:
            self.sources_status.setText("✅ Grabará: Micrófono + Sistema")
            self.sources_status.setStyleSheet("font-size: 10px; color: #4CAF50; margin-left: 5px;")
        elif mic_enabled:
            self.sources_status.setText("🎤 Grabará: Solo Micrófono")
            self.sources_status.setStyleSheet("font-size: 10px; color: #2196F3; margin-left: 5px;")
        elif system_enabled:
            self.sources_status.setText("🔊 Grabará: Solo Sistema")
            self.sources_status.setStyleSheet("font-size: 10px; color: #FF9800; margin-left: 5px;")
        
        # Habilitar/deshabilitar combos según selección
        self.input_combo.setEnabled(mic_enabled)
        self.test_input_btn.setEnabled(mic_enabled and self.input_combo.count() > 0)
        self.play_input_btn.setEnabled(mic_enabled and self.play_input_btn.isEnabled())
        
        self.output_combo.setEnabled(system_enabled)
        self.test_output_btn.setEnabled(system_enabled and self.output_combo.count() > 0)
        self.play_output_btn.setEnabled(system_enabled and self.play_output_btn.isEnabled())
    
    def test_device(self, device_type):
        """Inicia la prueba de un dispositivo."""
        if self.device_test_thread and self.device_test_thread.isRunning():
            self.device_test_thread.stop()
            self.device_test_thread.wait(1000)
        
        if device_type == 'input':
            combo = self.input_combo
            status_label = self.input_status
            test_btn = self.test_input_btn
            play_btn = self.play_input_btn
            other_test_btn = self.test_output_btn
        else:
            combo = self.output_combo
            status_label = self.output_status
            test_btn = self.test_output_btn
            play_btn = self.play_output_btn
            other_test_btn = self.test_input_btn
        
        current_index = combo.currentIndex()
        if current_index < 0:
            status_label.setText("❌ No hay dispositivo seleccionado")
            status_label.setStyleSheet("color: #ff4444;")
            return
        
        # Obtener información del dispositivo
        dev_id, dev_info = combo.itemData(current_index)
        
        # Actualizar UI
        test_btn.setText("Detener")
        test_btn.setEnabled(True)
        other_test_btn.setEnabled(False)
        play_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.test_progress.show()
        status_label.setText("🔄 Iniciando prueba...")
        status_label.setStyleSheet("color: #FFA500;")
        
        # Crear y conectar el hilo de prueba
        self.device_test_thread = DeviceTestThread(dev_id, dev_info, device_type)
        self.device_test_thread.test_completed.connect(
            lambda result: self.on_test_completed(device_type, result))
        self.device_test_thread.test_progress.connect(
            lambda msg: status_label.setText(f"🔄 {msg}"))
        self.device_test_thread.test_error.connect(
            lambda msg: self.on_test_error(device_type, msg))
        
        # Iniciar la prueba
        self.current_test = device_type
        self.device_test_thread.start()
    
    def on_test_completed(self, device_type, result):
        """Maneja la finalización de una prueba."""
        if device_type == 'input':
            status_label = self.input_status
            test_btn = self.test_input_btn
            play_btn = self.play_input_btn
            other_test_btn = self.test_output_btn
        else:
            status_label = self.output_status
            test_btn = self.test_output_btn
            play_btn = self.play_output_btn
            other_test_btn = self.test_input_btn
        
        # Actualizar UI según el resultado
        status_label.setText(result['message'])
        
        if result['status'] == 'success':
            status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        elif result['status'] == 'warning':
            status_label.setStyleSheet("color: #FFA500; font-weight: bold;")
        else:
            status_label.setStyleSheet("color: #ff4444; font-weight: bold;")
        
        # Guardar archivo de audio si existe
        if result.get('audio_file'):
            if device_type == 'input':
                self.input_audio_file = result['audio_file']
                play_btn.setEnabled(True)
                play_btn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 4px;")
            else:
                self.output_audio_file = result['audio_file']
                play_btn.setEnabled(True)
                play_btn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 4px;")
        
        # Restaurar controles
        test_btn.setText("Probar")
        test_btn.setEnabled(True)
        other_test_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.test_progress.hide()
        self.current_test = None
    
    def on_test_error(self, device_type, error_msg):
        """Maneja errores durante las pruebas."""
        if device_type == 'input':
            status_label = self.input_status
            test_btn = self.test_input_btn
            other_test_btn = self.test_output_btn
        else:
            status_label = self.output_status
            test_btn = self.test_output_btn
            other_test_btn = self.test_input_btn
            
        status_label.setText(f"❌ Error: {error_msg}")
        status_label.setStyleSheet("color: #ff4444; font-weight: bold;")
        
        # Restaurar controles
        test_btn.setText("Probar")
        test_btn.setEnabled(True)
        other_test_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.test_progress.hide()
        self.current_test = None
    
    def play_test_audio(self, device_type):
        """Reproduce el audio de prueba grabado."""
        try:
            if device_type == 'input':
                audio_file = self.input_audio_file
                play_btn = self.play_input_btn
            else:
                audio_file = self.output_audio_file
                play_btn = self.play_output_btn
            
            if not audio_file or not os.path.exists(audio_file):
                if hasattr(self.parent, 'show_status'):
                    self.parent.show_status("❌ No hay archivo de audio para reproducir", error=True)
                return
            
            # Cambiar botón temporalmente
            play_btn.setText("⏸")
            play_btn.setEnabled(False)
            
            # Cargar y reproducir audio
            samplerate, data = wavfile.read(audio_file)
            
            # Convertir a float32 si es necesario
            if data.dtype == np.int16:
                data = data.astype(np.float32) / 32767.0
            
            # Reproducir
            sd.play(data, samplerate=samplerate)
            
            # Restaurar botón después de la duración del audio
            duration_ms = int((len(data) / samplerate) * 1000) + 500
            QTimer.singleShot(duration_ms, lambda: self._restore_play_button(play_btn))
            
            if hasattr(self.parent, 'show_status'):
                self.parent.show_status("🔊 Reproduciendo audio de prueba...", error=False)
                
        except Exception as e:
            if hasattr(self.parent, 'show_status'):
                self.parent.show_status(f"❌ Error reproduciendo audio: {str(e)}", error=True)
            self._restore_play_button(play_btn)
    
    def _restore_play_button(self, play_btn):
        """Restaura el botón de reproducción."""
        play_btn.setText("▶")
        play_btn.setEnabled(True)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Configuración de la ventana principal
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName("MainWindow")
        self.setFixedSize(98, 40)
        self.radius = 19
        
        # Estados: ready, recording, paused, sending
        self.state = "ready"
        self.recorder = None
        
        # Crear widgets principales
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
        
        # Configuración inicial
        self._drag_pos = None
        self.recording_start_time = 0
        
        # Cargar configuración y verificar dispositivos
        self.config_panel.load_from_config(load_config())
        self._check_devices()
        self.update_ui()
    
    def _create_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Obtener la ruta base del directorio del script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Widget principal con fondo
        self.bg = QFrame(self)
        self.bg.setObjectName("MainWidget")
        self.bg.setGeometry(0, 0, 98, 40)
        
        # Etiqueta de estado
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color:#bbb; font-size:8px;")
        self.status_label.setFixedHeight(12)
        self.status_label.setVisible(False)
        
        # Timer para parpadeo
        self.blink_timer = QTimer(self)
        self.blink_on = False
        self.blink_timer.timeout.connect(self._toggle_blink)
        
        # Botón de grabación
        self.rec_btn = QPushButton()
        record_icon = os.path.join(base_dir, "assets", "icons", "record.svg")
        self.rec_btn.setIcon(QIcon(record_icon))
        self.rec_btn.setIconSize(QSize(18, 18))
        self.rec_btn.setFixedSize(50, 28)
        
        # Etiqueta de tiempo de grabación
        self.recording_time = QLabel("00:00")
        self.recording_time.setAlignment(Qt.AlignCenter)
        self.recording_time.setStyleSheet("color: #999; font-size: 9px;")
        self.recording_time.setVisible(False)
        
        # Botón de parar (oculto por defecto)
        self.stop_btn = QPushButton()
        stop_icon = os.path.join(base_dir, "assets", "icons", "stop.svg")
        self.stop_btn.setIcon(QIcon(stop_icon))
        self.stop_btn.setIconSize(QSize(18, 18))
        self.stop_btn.setFixedSize(24, 24)
        self.stop_btn.setVisible(False)
        
        # Botón de configuración
        self.settings_btn = QPushButton()
        self.settings_btn.setObjectName("SettingsButton")
        settings_icon = os.path.join(base_dir, "assets", "icons", "settings.svg")
        self.settings_btn.setIcon(QIcon(settings_icon))
        self.settings_btn.setIconSize(QSize(18, 18))
        self.settings_btn.setFixedSize(24, 24)
        
        # Panel de configuración
        self.config_panel = ConfigPanel(self)
        self.config_panel.setVisible(False)
        
        # Temporizador para el contador de grabación
        self.recording_timer = QTimer(self)
        self.recording_timer.timeout.connect(self.update_recording_time)
    
    def _setup_layout(self):
        """Configura el layout de la interfaz."""
        # Layout principal
        self.main_layout = QVBoxLayout(self.bg)
        self.main_layout.setContentsMargins(4, 0, 4, 0)
        self.main_layout.setSpacing(0)
        
        # Contenedor para el botón de grabación y el tiempo
        rec_btn_container = QVBoxLayout()
        rec_btn_container.setContentsMargins(0, 0, 0, 0)
        rec_btn_container.setSpacing(0)
        rec_btn_container.addWidget(self.rec_btn)
        rec_btn_container.addWidget(self.recording_time, alignment=Qt.AlignRight)
        
        # Controles de acción
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(4)
        controls_layout.addLayout(rec_btn_container)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addWidget(self.settings_btn)
        
        self.main_layout.addLayout(controls_layout)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.status_label, 0, Qt.AlignCenter)
        self.main_layout.addWidget(self.config_panel)
        
        # Animación para el panel de configuración
        self.anim = QPropertyAnimation(self.config_panel, b"maximumHeight")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.finished.connect(lambda: self.config_panel.setVisible(self.config_panel.maximumHeight() > 0))
    
    def _connect_signals(self):
        """Conecta todas las señales."""
        self.settings_btn.clicked.connect(self.open_config_panel)
        self.config_panel.save_btn.clicked.connect(self.save_config_panel)
        self.config_panel.close_btn.clicked.connect(self.close_application)
        self.rec_btn.clicked.connect(self.on_rec_btn)
        self.stop_btn.clicked.connect(self.on_stop_btn)
    
    def _check_devices(self):
        """Verifica si hay dispositivos de audio disponibles."""
        try:
            devices = get_audio_devices()
            has_input = any('input' in dev['type'] for dev in devices)
            has_output = any('output' in dev['type'] for dev in devices)
            
            if not has_input:
                self.show_status("No se encontraron dispositivos de entrada", error=True)
            if not has_output:
                self.show_status("No se encontraron dispositivos de salida", error=True)
                
        except Exception as e:
            self.show_status(f"Error al verificar dispositivos: {str(e)}", error=True)
    
    def update_ui(self):
        """Actualiza la interfaz según el estado actual."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Cargar íconos
        record_icon = QIcon(os.path.join(base_dir, "assets", "icons", "record.svg"))
        pause_icon = QIcon(os.path.join(base_dir, "assets", "icons", "pause.svg"))
        play_icon = QIcon(os.path.join(base_dir, "assets", "icons", "play.svg"))
        
        # Actualizar según el estado
        if self.state == "ready":
            self.rec_btn.setIcon(record_icon)
            self.rec_btn.setEnabled(True)
            self.stop_btn.setVisible(False)
            self.settings_btn.setEnabled(True)
            self.settings_btn.setVisible(True)
            self.recording_time.setVisible(False)
            self.blink_timer.stop()
            self.rec_btn.setStyleSheet("")
            
        elif self.state == "recording":
            self.rec_btn.setIcon(pause_icon)
            self.rec_btn.setEnabled(True)
            self.stop_btn.setVisible(True)
            self.settings_btn.setEnabled(False)
            self.settings_btn.setVisible(False)
            self.recording_time.setVisible(True)
            self.blink_on = False
            self.blink_timer.start(500)
            
        elif self.state == "paused":
            self.rec_btn.setIcon(play_icon)
            self.rec_btn.setEnabled(True)
            self.stop_btn.setVisible(True)
            self.settings_btn.setEnabled(False)
            self.settings_btn.setVisible(False)
            self.recording_time.setVisible(True)
            self.blink_timer.stop()
            self.rec_btn.setStyleSheet("background-color: rgba(220,220,40,120);")
            
        elif self.state == "sending":
            self.rec_btn.setEnabled(False)
            self.stop_btn.setVisible(False)
            self.settings_btn.setEnabled(False)
            self.settings_btn.setVisible(False)
            self.recording_time.setVisible(False)
            self.blink_timer.stop()
            self.rec_btn.setStyleSheet("")
        
        self.status_label.setVisible(False)
    
    def show_status(self, msg, error=False):
        """Muestra un mensaje de estado."""
        self.status_label.setText(msg)
        self.status_label.setStyleSheet(f"color:{'#f55' if error else '#bbb'};font-size:12px;")
        self.status_label.setVisible(True)
        QTimer.singleShot(3000, lambda: self.status_label.setVisible(False))
    
    def _toggle_blink(self):
        """Alterna el estado del parpadeo del botón de grabación."""
        self.blink_on = not self.blink_on
        if self.blink_on:
            self.rec_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff4444;
                    border-radius: 14px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #ff6666;
                }
            """)
        else:
            self.rec_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff0000;
                    border-radius: 14px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #ff3333;
                }
            """)
    
    def on_rec_btn(self):
        """Maneja el clic en el botón de grabación."""
        if self.state == "ready":
            config = load_config()
            
            # Obtener configuración
            mic_index = config.get('input_device')
            sys_index = config.get('output_device')
            webhook_url = config.get('webhook_url', '')
            chunk_duration = config.get('chunk_duration', 4)
            
            # Obtener configuración de fuentes de grabación
            record_microphone = config.get('record_microphone', True)
            record_system = config.get('record_system', True)
            
            # Aplicar selección de fuentes
            if not record_microphone:
                mic_index = None
            if not record_system:
                sys_index = None
            
            # Crear y configurar el recorder
            self.recorder = AudioRecorder(
                mic_index=mic_index,
                sys_index=sys_index,
                webhook_url=webhook_url,
                chunk_duration=chunk_duration
            )
            
            # Conectar señales
            self.recorder.recording_started.connect(self.on_recording_started)
            self.recorder.recording_finished.connect(self.on_recording_finished)
            self.recorder.status_update.connect(self.show_status)
            self.recorder.finished_sending.connect(self.on_finished_sending)
            self.recorder.error_occurred.connect(self.on_error)
            
            # Iniciar grabación
            self.recorder.start()
            self.state = "recording"
            self.update_ui()
    
    def on_stop_btn(self):
        """Maneja el clic en el botón de parar."""
        if self.state == "recording" and self.recorder:
            self.recorder.stop_recording()
            self.recorder.wait(3000)
            self.state = "ready"
            self.update_ui()
    
    def on_recording_started(self):
        """Se ejecuta cuando inicia la grabación."""
        self.recording_start_time = time.time()
        self.recording_timer.start(1000)
        self.state = "recording"
        self.update_ui()
    
    def on_recording_finished(self, path):
        """Se ejecuta cuando termina la grabación."""
        self.recording_timer.stop()
        self.recording_time.setText("00:00")
        self.show_status("Grabación finalizada.")
        self.state = "ready"
        self.update_ui()
    
    def on_finished_sending(self, success, chunk_id):
        """Se ejecuta cuando se envía un chunk."""
        if success:
            self.show_status(f"Chunk {chunk_id} enviado.")
        else:
            self.show_status(f"Error al enviar {chunk_id}.", error=True)
    
    def on_error(self, msg):
        """Se ejecuta cuando hay un error."""
        self.show_status(f"Error: {msg}", error=True)
        self.state = "ready"
        self.update_ui()
    
    def update_recording_time(self):
        """Actualiza el tiempo de grabación."""
        if self.state == "recording" and hasattr(self, 'recording_start_time'):
            elapsed = int(time.time() - self.recording_start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.recording_time.setText(f"{minutes:02d}:{seconds:02d}")
    
    def toggle_config(self):
        """Expande o colapsa el panel de configuración."""
        collapsed = (not self.config_panel.isVisible()) or self.config_panel.maximumHeight() == 0
        
        self.anim.stop()
        
        if collapsed:
            # Expandir panel
            self.config_panel.setVisible(True)
            self.config_panel.setMaximumHeight(0)
            self.anim.setStartValue(0)
            self.anim.setEndValue(500)
            self.setFixedSize(800, 540)
        else:
            # Colapsar panel
            current_h = self.config_panel.maximumHeight()
            self.anim.setStartValue(current_h)
            self.anim.setEndValue(0)
            self.setFixedSize(98, 40)
        
        self.anim.start()
    
    def open_config_panel(self):
        """Abre el panel de configuración."""
        self.config_panel.load_from_config(load_config())
        self.toggle_config()
    
    def save_config_panel(self):
        """Guarda la configuración del panel."""
        self.config_panel.save_to_config()
        self.show_status("Configuración guardada", error=False)
        self._check_devices()
        self.toggle_config()
    
    def close_application(self):
        """Cierra la aplicación completamente."""
        if self.recorder and self.recorder.isRunning():
            self.recorder.stop_recording()
            self.recorder.wait(2000)
        QApplication.quit()
    
    def resizeEvent(self, event):
        """Se ejecuta cuando se redimensiona la ventana."""
        super().resizeEvent(event)
        self.bg.setGeometry(0, 0, self.width(), self.height())
    
    def mousePressEvent(self, event):
        """Inicia el arrastre de la ventana."""
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Mueve la ventana durante el arrastre."""
        if event.buttons() == Qt.LeftButton and self._drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Termina el arrastre de la ventana."""
        self._drag_pos = None
    
    def paintEvent(self, event):
        """Dibuja la ventana con esquinas redondeadas."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)
        painter.fillPath(path, QColor(40, 40, 40, 200))
        
        # Borde
        pen = QPen(QColor(80, 80, 80), 1)
        painter.setPen(pen)
        painter.drawPath(path)

def load_style(app):
    """Carga el archivo de estilos si existe."""
    if os.path.exists(STYLE_PATH):
        with open(STYLE_PATH, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())

def main():
    app = QApplication(sys.argv)
    load_style(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
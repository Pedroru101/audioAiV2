#!/usr/bin/env python3
"""
🔍 TESTER DE DISPOSITIVOS DE AUDIO
Diagnóstico completo de dispositivos de audio
"""

import sounddevice as sd
import numpy as np

def get_audio_devices():
    """Obtener lista de dispositivos de audio disponibles"""
    try:
        devices = sd.query_devices()
        device_list = []
        
        for i, device in enumerate(devices):
            device_info = {
                'id': i,
                'name': device['name'],
                'max_input_channels': device['max_input_channels'],
                'max_output_channels': device['max_output_channels'],
                'default_samplerate': device.get('default_samplerate', 44100),
                'hostapi': sd.query_hostapis(device['hostapi'])['name'],
                'type': []
            }
            
            if device['max_input_channels'] > 0:
                device_info['type'].append('input')
            if device['max_output_channels'] > 0:
                device_info['type'].append('output')
                
            device_list.append(device_info)
        
        return device_list
    except Exception as e:
        print(f"Error obteniendo dispositivos: {e}")
        return []

class AudioDeviceTester:
    """Clase para probar dispositivos de audio"""
    
    def __init__(self):
        pass
    
    def test_device(self, device_id, test_type='input', duration=3):
        """Probar un dispositivo específico"""
        try:
            devices = sd.query_devices()
            if device_id >= len(devices):
                return {'success': False, 'error': 'Device ID invalid'}
            
            device = devices[device_id]
            
            if test_type == 'input' and device['max_input_channels'] == 0:
                return {'success': False, 'error': 'Device has no input channels'}
            
            if test_type == 'output' and device['max_output_channels'] == 0:
                return {'success': False, 'error': 'Device has no output channels'}
            
            # Probar el dispositivo
            samplerate = int(device.get('default_samplerate', 44100))
            
            if test_type == 'input':
                channels = min(2, device['max_input_channels'])
                
                with sd.InputStream(
                    device=device_id,
                    channels=channels,
                    samplerate=samplerate,
                    dtype='float32'
                ) as stream:
                    audio_data = stream.read(samplerate * duration)[0]
                    
                    max_level = np.max(np.abs(audio_data))
                    avg_level = np.mean(np.abs(audio_data))
                    
                    return {
                        'success': True,
                        'max_level': float(max_level),
                        'avg_level': float(avg_level),
                        'channels': channels,
                        'samplerate': samplerate,
                        'duration': duration
                    }
            
            else:  # output test
                # Generar tono de prueba
                frequency = 440
                t = np.linspace(0, duration, int(samplerate * duration), False)
                tone = 0.3 * np.sin(2 * np.pi * frequency * t)
                
                sd.play(tone, samplerate, device=device_id)
                sd.wait()
                
                return {
                    'success': True,
                    'message': 'Tone played successfully',
                    'frequency': frequency,
                    'duration': duration
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

def test_all_audio_devices():
    print("🔍 DIAGNÓSTICO COMPLETO DE DISPOSITIVOS DE AUDIO")
    print("=" * 70)
    
    devices = sd.query_devices()
    
    print("📱 TODOS LOS DISPOSITIVOS:")
    print("-" * 50)
    
    input_devices = []
    output_devices = []
    
    for i, device in enumerate(devices):
        name = device['name']
        max_in = device['max_input_channels']
        max_out = device['max_output_channels']
        sample_rate = device.get('default_samplerate', 0)
        
        device_type = []
        if max_in > 0:
            device_type.append(f"IN:{max_in}")
            input_devices.append((i, device))
        if max_out > 0:
            device_type.append(f"OUT:{max_out}")
            output_devices.append((i, device))
        
        type_str = " | ".join(device_type) if device_type else "NONE"
        
        print(f"ID {i:2d}: {name[:40]:<40} [{type_str}] {sample_rate}Hz")
        
        if 'VB-Audio' in name or 'CABLE' in name:
            print(f"      🎯 VB-AUDIO DETECTADO")
    
    print(f"\n📊 RESUMEN:")
    print(f"   Dispositivos de entrada: {len(input_devices)}")
    print(f"   Dispositivos de salida: {len(output_devices)}")
    
    # Verificar dispositivo de salida actual
    print(f"\n🔊 DISPOSITIVO DE SALIDA PREDETERMINADO:")
    try:
        default_output = sd.query_devices(kind='output')
        print(f"   {default_output['name']}")
        
        if 'CABLE' in default_output['name']:
            print("   ✅ VB-Audio está configurado como salida predeterminada")
        else:
            print("   ⚠️  VB-Audio NO está configurado como salida predeterminada")
            print("   💡 Cambia la salida a 'CABLE Input' en Windows")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Verificar dispositivo de entrada actual
    print(f"\n🎤 DISPOSITIVO DE ENTRADA PREDETERMINADO:")
    try:
        default_input = sd.query_devices(kind='input')
        print(f"   {default_input['name']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Probar captura de micrófono normal
    print(f"\n🧪 PRUEBA DE MICRÓFONO NORMAL:")
    print("   Habla por 3 segundos...")
    
    try:
        with sd.InputStream(channels=1, samplerate=44100, dtype='float32') as stream:
            audio_data = stream.read(44100 * 3)[0]  # 3 segundos
            
            max_level = np.max(np.abs(audio_data))
            avg_level = np.mean(np.abs(audio_data))
            
            print(f"   📊 Nivel máximo: {max_level:.6f}")
            print(f"   📊 Nivel promedio: {avg_level:.6f}")
            
            if max_level > 0.01:
                print("   ✅ Micrófono funciona correctamente")
            else:
                print("   ⚠️  Micrófono muy bajo o sin audio")
                
    except Exception as e:
        print(f"   ❌ Error en micrófono: {e}")
    
    # Generar tono de prueba
    print(f"\n🔊 GENERANDO TONO DE PRUEBA:")
    print("   Reproduciendo tono de 440Hz por 2 segundos...")
    
    try:
        # Generar tono
        duration = 2
        samplerate = 44100
        frequency = 440
        
        t = np.linspace(0, duration, int(samplerate * duration), False)
        tone = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        sd.play(tone, samplerate)
        sd.wait()
        
        print("   ✅ Tono reproducido")
        print("   💡 Si escuchaste el tono, el audio de salida funciona")
        
    except Exception as e:
        print(f"   ❌ Error reproduciendo tono: {e}")
    
    return True



if __name__ == "__main__":
    test_all_audio_devices()
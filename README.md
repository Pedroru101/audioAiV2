# 🎵 Audio Capture Widget

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://github.com/yourusername/audio-capture-widget)

Aplicación profesional de grabación de audio simultánea de micrófono y sistema con interfaz flotante minimalista y funcionalidades avanzadas.

![Audio Capture Widget Screenshot](assets/app_icon.jpg)

## ✨ Características Principales

- 🎤 **Grabación Simultánea**: Micrófono y audio del sistema en tiempo real
- 🎯 **Selección de Fuentes**: Elige grabar solo micrófono, solo sistema, o ambos
- 🔊 **Prueba de Dispositivos**: Grabación de 3 segundos con reproducción instantánea
- 📦 **Chunks Automáticos**: Configurables de 2-300 segundos
- 🌐 **Integración Webhook**: Compatible con n8n y otros sistemas
- 🎨 **Interfaz Flotante**: Minimalista, arrastrable y siempre visible
- ⚙️ **Panel de Configuración**: Animado con opciones avanzadas
- 🔄 **Mezcla Inteligente**: Audio en tiempo real con normalización automática
- 📱 **Ejecutable Standalone**: No requiere Python instalado

## 🚀 Instalación

### Opción 1: Ejecutable (Recomendado)
1. Descargar el [último release](https://github.com/yourusername/audio-capture-widget/releases)
2. Ejecutar `AudioCaptureWidget.exe`
3. ¡Listo para usar!

### Opción 2: Desde Código Fuente

#### 1. Clonar el repositorio
```bash
git clone https://github.com/yourusername/audio-capture-widget.git
cd audio-capture-widget
```

#### 2. Crear entorno virtual
```bash
python -m venv venv
```

#### 3. Activar entorno virtual
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac (experimental)
source venv/bin/activate
```

#### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 5. Ejecutar la aplicación
```bash
python main.py
```

## 🎯 Guía de Uso

### 🎬 Inicio Rápido
1. **Ejecutar**: Doble clic en `AudioCaptureWidget.exe` o `python main.py`
2. **Configurar**: Presiona el botón ⚙️ para abrir configuración
3. **Seleccionar fuentes**: Marca los checkboxes según necesites:
   - ☑️ **Solo Micrófono**: Grabación de voz/ambiente
   - ☑️ **Solo Sistema**: Captura audio de aplicaciones
   - ☑️ **Ambos**: Grabación completa (recomendado)
4. **Probar dispositivos**: Usa los botones "Probar" y "▶" para verificar
5. **Grabar**: Presiona 🎤 para iniciar, 🛑 para detener

### ⚙️ Configuración Avanzada

#### Dispositivos de Audio
1. **Micrófono**: Selecciona tu dispositivo de entrada preferido
2. **Sistema**: Para captura de sistema, recomendamos VB-Audio Cable
3. **Pruebas**: Cada dispositivo se puede probar independientemente

#### Opciones de Grabación
- **Webhook URL**: Envío automático a n8n u otros servicios
- **Duración de Chunks**: Segmentos de 2-300 segundos
- **Fuentes Flexibles**: Combina o separa micrófono y sistema

#### Configuración de Sistema
Para captura de audio del sistema:
1. Instalar [VB-Audio Cable](https://vb-audio.com/Cable/)
2. Configurar aplicaciones para usar "CABLE Input"
3. Seleccionar "CABLE Output" en la aplicación

## 📁 Estructura del Proyecto

```
Audio.ai.V2/
├── main.py                 # Aplicación principal
├── audio_handler.py        # Motor de grabación
├── audio_device_tester.py  # Prueba de dispositivos
├── utils.py               # Utilidades
├── config.json            # Configuración
├── requirements.txt       # Dependencias
├── assets/               # Recursos
│   ├── icons/           # Iconos SVG
│   └── styles/          # Estilos CSS
├── temp_audio/          # Archivos temporales
├── grabaciones/         # Grabaciones finales
└── venv/               # Entorno virtual
```

## ⚙️ Configuración

El archivo `config.json` contiene:

```json
{
  "input_device": 2,           // ID del micrófono
  "output_device": 1,          // ID del dispositivo de sistema
  "webhook_url": "http://...", // URL del webhook
  "chunk_duration": 4          // Duración en segundos
}
```

## 🔧 Dispositivos Recomendados

### Para Micrófono:
- Cualquier dispositivo de entrada estándar
- Preferir dispositivos WASAPI o MME

### Para Audio del Sistema:
- Dispositivos con "loopback" en el nombre
- VB-Audio Cable (recomendado)
- "Stereo Mix" o "What U Hear" (si está habilitado)

## 🆘 Solución de Problemas

### No se detecta audio del sistema:
1. Instalar VB-Audio Cable
2. Configurar aplicaciones para usar "CABLE Input"
3. Seleccionar "CABLE Output" en la aplicación

### Errores de "Input Overflow":
1. Usar dispositivos MME en lugar de WASAPI
2. Aumentar chunk_duration a 8-10 segundos
3. Cerrar otras aplicaciones de audio

### Botón de parar no aparece:
- Verificar que la configuración esté guardada correctamente
- Reiniciar la aplicación

## 📦 Dependencias

- **PySide6**: Interfaz gráfica
- **sounddevice**: Grabación de audio
- **numpy**: Procesamiento numérico
- **scipy**: Análisis de audio
- **pydub**: Manipulación de audio (opcional)
- **lameenc**: Codificación MP3 (opcional)
- **requests**: Envío a webhook

## 🎵 Formatos Soportados

- **Salida**: WAV, MP3 (si pydub está disponible)
- **Calidad**: 44100Hz, 16-bit, mono/estéreo
- **Compresión**: MP3 128kbps (configurable)

## 🔄 Flujo de Trabajo

1. **Configuración** → Prueba de dispositivos
2. **Grabación** → Chunks automáticos cada X segundos
3. **Procesamiento** → Mezcla micrófono + sistema
4. **Envío** → Webhook automático (opcional)
5. **Almacenamiento** → Archivos locales en temp_audio/

## 📞 Soporte

Para problemas o sugerencias, revisar:
1. Configuración de dispositivos en el panel
2. Logs de la aplicación
3. Permisos de micrófono del sistema
4. Configuración de VB-Audio Cable

## 🏗️ Construcción del Ejecutable

Para crear tu propio ejecutable:

```bash
# Instalar PyInstaller
pip install PyInstaller

# Construir ejecutable
python build.py

# El ejecutable estará en dist/AudioCaptureWidget.exe
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Changelog

### v1.0.0 (2024-07-22)
- ✨ Selección flexible de fuentes de grabación
- 🎤 Prueba independiente de dispositivos
- 🔊 Soporte mejorado para VB-Audio Cable
- 📦 Empaquetado en ejecutable standalone
- 🧹 Proyecto limpio y optimizado
- 📚 Documentación completa

## 🐛 Problemas Conocidos

- **Windows Defender**: Puede marcar el ejecutable como sospechoso (falso positivo)
- **Permisos de Micrófono**: Windows puede solicitar permisos la primera vez
- **VB-Audio**: Requiere instalación separada para captura de sistema

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- [PySide6](https://pypi.org/project/PySide6/) - Framework de interfaz gráfica
- [sounddevice](https://pypi.org/project/sounddevice/) - Captura de audio
- [VB-Audio](https://vb-audio.com/) - Soluciones de audio virtual
- [PyInstaller](https://pyinstaller.org/) - Empaquetado de aplicaciones

## 📞 Soporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/audio-capture-widget/issues)
- 💬 **Discusiones**: [GitHub Discussions](https://github.com/yourusername/audio-capture-widget/discussions)
- 📧 **Email**: tu-email@ejemplo.com

---

**Desarrollado con ❤️ para grabación de audio profesional**

⭐ **¡Dale una estrella si te gusta el proyecto!** ⭐
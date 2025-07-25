# ðŸŽµ Audio Capture Widget

<div align="center">

![Audio Capture Widget](assets/app_icon.jpg)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg?style=for-the-badge&logo=qt)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg?style=for-the-badge&logo=windows)](https://github.com/Pedroru101/audioAiV2)

**ðŸš€ AplicaciÃ³n profesional de grabación de audio simultÃ¡nea ðŸŽ¤ðŸ”Š**

*Interfaz flotante minimalista con funcionalidades avanzadas*

[ðŸ“¥ Descargar](#-instalaciÃ³n) â€¢ [ðŸ“– DocumentaciÃ³n](#-guÃ­a-de-uso) â€¢ [ðŸ› Reportar Bug](https://github.com/Pedroru101/audioAiV2/issues) â€¢ [ðŸ’¡ Sugerir Feature](https://github.com/Pedroru101/audioAiV2/discussions)

</div>

---

## âœ¨ CaracterÃ­sticas Principales

<table>
<tr>
<td width="50%">

### ðŸŽ¤ **grabación Avanzada**
- ðŸŽ¯ **grabación SimultÃ¡nea**: MicrÃ³fono + Sistema
- ðŸ”€ **selección Flexible**: Solo mic, solo sistema, o ambos
- ðŸ“Š **Calidad Profesional**: 44.1kHz, 16-bit
- ðŸ”„ **Mezcla Inteligente**: NormalizaciÃ³n automÃ¡tica

</td>
<td width="50%">

### ðŸŽ¨ **Interfaz Moderna**
- ðŸªŸ **Ventana Flotante**: Siempre visible
- ðŸŽ­ **Minimalista**: DiseÃ±o limpio y elegante
- ðŸ–±ï¸ **Arrastrable**: Posiciona donde quieras
- âš™ï¸ **Panel Animado**: Configuración intuitiva

</td>
</tr>
<tr>
<td width="50%">

### ðŸ”§ **Funcionalidades Pro**
- ðŸ§ª **Prueba de Dispositivos**: Test de 3 segundos
- â–¶ï¸ **ReproducciÃ³n InstantÃ¡nea**: Escucha tus pruebas
- ðŸ“¦ **Chunks Configurables**: 2-300 segundos
- ðŸŒ **Webhook Integration**: n8n compatible

</td>
<td width="50%">

### ðŸš€ **DistribuciÃ³n**
- ðŸ“± **Ejecutable Standalone**: Sin Python requerido
- ðŸ”’ **Seguro**: Sin dependencias externas
- âš¡ **RÃ¡pido**: Inicio instantÃ¡neo
- ðŸŽ¯ **Optimizado**: TamaÃ±o mÃ­nimo

</td>
</tr>
</table>

---

## ðŸŽ¬ Demo Visual

<div align="center">

### 🎯 **Interfaz Principal & Panel de Configuración**
![Interfaz de Configuración](Imgapp.jpg)
*Panel de Configuración completo con selección de dispositivos, fuentes de grabación y Configuración de webhook para n8n*

### ðŸŽ¤ **Widget Flotante Minimalista**
![Widget Flotante](Imgwi.jpg)
*Interfaz flotante compacta con controles esenciales: Grabar, Config y Status - Siempre visible durante el trabajo*

**ðŸŽ¨ CaracterÃ­sticas Visuales:**
- âœ¨ **Interfaz oscura profesional** - DiseÃ±o moderno que no cansa la vista
- ðŸŽ¯ **Controles intuitivos** - Botones grandes y accesibles para uso rÃ¡pido
- ðŸ”„ **Animaciones suaves** - Transiciones elegantes entre estados
- ðŸ“± **DiseÃ±o arrastrable** - Posiciona el widget donde lo necesites
- âš™ï¸ **Panel expandible** - Configuración completa sin saturar la interfaz
- ðŸŽ›ï¸ **Configuración visual** - selección de dispositivos con pruebas en tiempo real

</div>

---

## ðŸ“¥ InstalaciÃ³n

### ðŸš€ OpciÃ³n 1: Ejecutable (Recomendado)

<div align="center">

**ðŸŽ¯ Â¡La forma mÃ¡s fÃ¡cil!**

[![Download](https://img.shields.io/badge/ðŸ“¥_Descargar-Ejecutable-success?style=for-the-badge&logo=download)](https://github.com/Pedroru101/audioAiV2/releases)

</div>

1. ðŸ“¥ **Descargar** el [Ãºltimo release](https://github.com/Pedroru101/audioAiV2/releases)
2. ðŸ–±ï¸ **Ejecutar** `AudioCaptureWidget.exe`
3. ðŸŽ‰ **Â¡Listo para usar!**

### ðŸ› ï¸ OpciÃ³n 2: Desde CÃ³digo Fuente

<details>
<summary>ðŸ‘¨â€ðŸ’» <strong>Para Desarrolladores</strong> (Click para expandir)</summary>

#### 1ï¸âƒ£ Clonar el repositorio
```bash
git clone https://github.com/Pedroru101/audioAiV2.git
cd audioAiV2
```

#### 2ï¸âƒ£ Crear entorno virtual
```bash
python -m venv venv
```

#### 3ï¸âƒ£ Activar entorno virtual
```bash
# ðŸªŸ Windows
.\venv\Scripts\activate

# ðŸ§ Linux/Mac
source venv/bin/activate
```

#### 4ï¸âƒ£ Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 5ï¸âƒ£ Ejecutar la aplicaciÃ³n
```bash
python main.py
```

</details>

---

## ðŸŽ¯ GuÃ­a de Uso

### ðŸš€ Inicio RÃ¡pido

<div align="center">

```mermaid
graph LR
    A[ðŸš€ Ejecutar App] --> B[âš™ï¸ Configurar]
    B --> C[ðŸŽ¯ Seleccionar Fuentes]
    C --> D[ðŸ§ª Probar Dispositivos]
    D --> E[ðŸŽ¤ Grabar]
    E --> F[ðŸ›‘ Detener]
    F --> G[ðŸ“ Archivos Listos]
```

</div>

#### 1ï¸âƒ£ **Ejecutar**
- ðŸ–±ï¸ Doble clic en `AudioCaptureWidget.exe`
- âš¡ O ejecuta `python main.py`

#### 2ï¸âƒ£ **Configurar**
- âš™ï¸ Presiona el botÃ³n de Configuración
- ðŸŽ¨ Se abre el panel animado

#### 3ï¸âƒ£ **Seleccionar Fuentes**
Elige quÃ© grabar segÃºn tus necesidades:

<table>
<tr>
<td align="center">

**ðŸŽ¤ Solo MicrÃ³fono**
```
â˜‘ï¸ ðŸŽ¤ Grabar MicrÃ³fono
â˜ ðŸ”Š Grabar Sistema
```
*Perfecto para podcasts, voces*

</td>
<td align="center">

**ðŸ”Š Solo Sistema**
```
â˜ ðŸŽ¤ Grabar MicrÃ³fono  
â˜‘ï¸ ðŸ”Š Grabar Sistema
```
*Ideal para mÃºsica, videos*

</td>
<td align="center">

**ðŸŽµ Ambos (Recomendado)**
```
â˜‘ï¸ ðŸŽ¤ Grabar MicrÃ³fono
â˜‘ï¸ ðŸ”Š Grabar Sistema
```
*grabación completa*

</td>
</tr>
</table>

#### 4ï¸âƒ£ **Probar Dispositivos**
- ðŸ§ª Usa los botones **"Probar"** para test de 3 segundos
- â–¶ï¸ Presiona **"â–¶"** para escuchar las grabaciones
- âœ… Verifica que todo funcione correctamente

#### 5ï¸âƒ£ **Grabar**
- ðŸŽ¤ Presiona el botÃ³n de **GRABAR**
- ðŸ›‘ Aparece el botÃ³n de **DETENER**
- ðŸ“Š Observa el estado en tiempo real

---

## âš™ï¸ Configuración Avanzada

### ðŸŽ¤ Dispositivos de Audio

<div align="center">

| Tipo | RecomendaciÃ³n | DescripciÃ³n |
|------|---------------|-------------|
| ðŸŽ¤ **MicrÃ³fono** | Cualquier dispositivo estÃ¡ndar | WASAPI o MME preferido |
| ðŸ”Š **Sistema** | VB-Audio Cable | Para captura de aplicaciones |
| ðŸŽ§ **Monitoreo** | Auriculares/Altavoces | Para escuchar pruebas |

</div>

### ðŸ”Š Configuración de Sistema Audio

<details>
<summary>ðŸ› ï¸ <strong>Setup VB-Audio Cable</strong> (Recomendado)</summary>

#### ðŸ“¥ InstalaciÃ³n
1. ðŸŒ Descargar [VB-Audio Cable](https://vb-audio.com/Cable/)
2. ðŸ”§ Instalar como administrador
3. ðŸ”„ Reiniciar el sistema

#### âš™ï¸ Configuración
1. ðŸŽµ **En tus aplicaciones** (Spotify, YouTube, etc.):
   - Seleccionar **"CABLE Input"** como salida de audio
2. ðŸŽ¤ **En Audio Capture Widget**:
   - Seleccionar **"CABLE Output"** como dispositivo de sistema

#### âœ… VerificaciÃ³n
```
AplicaciÃ³n â†’ CABLE Input â†’ CABLE Output â†’ Audio Capture Widget
```

</details>

### ðŸŒ Webhook Configuration

<div align="center">

**ðŸ”— IntegraciÃ³n con n8n y otros servicios**

</div>

```json
{
  "webhook_url": "http://localhost:5678/webhook/audio",
  "chunk_duration": 4,
  "auto_send": true
}
```

---

## ðŸ“ Estructura del Proyecto

<div align="center">

```
ðŸŽµ Audio Capture Widget/
â”œâ”€â”€ ðŸš€ main.py                 # AplicaciÃ³n principal
â”œâ”€â”€ ðŸŽ¤ audio_handler.py        # Motor de grabación
â”œâ”€â”€ ðŸ§ª audio_device_tester.py  # Prueba de dispositivos
â”œâ”€â”€ ðŸ”§ utils.py                # Utilidades
â”œâ”€â”€ ðŸ—ï¸ build.py                # Script de construcciÃ³n
â”œâ”€â”€ ðŸ“¦ create_distribution.py  # Creador de paquetes
â”œâ”€â”€ âš™ï¸ config.json             # Configuración
â”œâ”€â”€ ðŸ“‹ requirements.txt        # Dependencias
â”œâ”€â”€ ðŸ“– CONTRIBUTING.md         # GuÃ­a de contribuciÃ³n
â”œâ”€â”€ ðŸ“„ LICENSE                 # Licencia MIT
â”œâ”€â”€ ðŸ–¼ï¸ Imgapp.jpg              # Captura del panel de Configuración
â”œâ”€â”€ ï¿½ï¸ Imgwi.jpog               # Captura del widget flotante
â”œâ”€â”€ ðŸŽ¨ assets/                 # Recursos (si existe)
â”œâ”€â”€ ðŸ“ grabaciones/            # Grabaciones finales
â””â”€â”€ ðŸ“ .github/                # Configuración de GitHub
    â”œâ”€â”€ ðŸ”§ workflows/          # GitHub Actions
    â”œâ”€â”€ ðŸ“‹ ISSUE_TEMPLATE/     # Templates de issues
    â””â”€â”€ ðŸ‘¥ CODEOWNERS          # Propietarios del cÃ³digo
```

</div>

---

## ðŸ”§ Configuración JSON

<details>
<summary>âš™ï¸ <strong>Archivo config.json</strong></summary>

```json
{
  "input_device": 2,           // ðŸŽ¤ ID del micrÃ³fono
  "output_device": 1,          // ðŸ”Š ID del dispositivo de sistema
  "webhook_url": "http://...", // ðŸŒ URL del webhook
  "chunk_duration": 4,         // â±ï¸ DuraciÃ³n en segundos
  "record_microphone": true,   // ðŸŽ¤ Habilitar micrÃ³fono
  "record_system": true        // ðŸ”Š Habilitar sistema
}
```

</details>

---

## ðŸ†˜ SoluciÃ³n de Problemas

<div align="center">

### ðŸš¨ Problemas Comunes y Soluciones

</div>

<details>
<summary>ðŸ”Š <strong>No se detecta audio del sistema</strong></summary>

#### ðŸ” DiagnÃ³stico
- âŒ VB-Audio Cable no instalado
- âŒ Configuración incorrecta de aplicaciones
- âŒ Dispositivo incorrecto seleccionado

#### âœ… SoluciÃ³n
1. ðŸ“¥ Instalar [VB-Audio Cable](https://vb-audio.com/Cable/)
2. âš™ï¸ Configurar aplicaciones para usar **"CABLE Input"**
3. ðŸŽ¯ Seleccionar **"CABLE Output"** en la aplicaciÃ³n
4. ðŸ§ª Probar con el botÃ³n **"Test"**

</details>

<details>
<summary>âš ï¸ <strong>Errores de "Input Overflow"</strong></summary>

#### ðŸ” SÃ­ntomas
- âŒ Audio cortado o distorsionado
- âŒ Mensajes de overflow en logs
- âŒ grabación interrumpida

#### âœ… SoluciÃ³n
1. ðŸ”„ Usar dispositivos **MME** en lugar de **WASAPI**
2. â±ï¸ Aumentar `chunk_duration` a **8-10 segundos**
3. âŒ Cerrar otras aplicaciones de audio
4. ðŸ”§ Reducir calidad de audio si es necesario

</details>

<details>
<summary>ðŸ›‘ <strong>BotÃ³n de parar no aparece</strong></summary>

#### ðŸ” Posibles Causas
- âŒ Configuración no guardada
- âŒ Dispositivos no seleccionados
- âŒ Error en inicializaciÃ³n

#### âœ… SoluciÃ³n
1. âœ… Verificar que la Configuración estÃ© guardada
2. ðŸ”„ Reiniciar la aplicaciÃ³n
3. ðŸ§ª Probar dispositivos antes de grabar
4. ðŸ“‹ Revisar logs para errores

</details>

---

## ðŸ“¦ Dependencias

<div align="center">

### ðŸ› ï¸ Stack TecnolÃ³gico

</div>

<table>
<tr>
<td align="center">

**ðŸ–¼ï¸ Interfaz**
- ðŸŽ¨ **PySide6**: Framework GUI
- ðŸŽ­ **Qt**: Widgets y animaciones

</td>
<td align="center">

**ðŸŽµ Audio**
- ðŸŽ¤ **sounddevice**: Captura de audio
- ðŸ”¢ **numpy**: Procesamiento numÃ©rico
- ðŸ“Š **scipy**: AnÃ¡lisis de audio

</td>
<td align="center">

**ðŸ”§ Utilidades**
- ðŸŽµ **pydub**: ManipulaciÃ³n de audio
- ðŸŽ¼ **lameenc**: CodificaciÃ³n MP3
- ðŸŒ **requests**: ComunicaciÃ³n webhook

</td>
</tr>
</table>

---

## ðŸŽµ Formatos Soportados

<div align="center">

| Formato | Calidad | Uso Recomendado |
|---------|---------|-----------------|
| ðŸŽµ **WAV** | 44.1kHz, 16-bit | MÃ¡xima calidad |
| ðŸŽ¼ **MP3** | 128kbps | DistribuciÃ³n web |
| ðŸ”Š **Mono/EstÃ©reo** | Configurable | SegÃºn necesidad |

</div>

---

## ðŸ”„ Flujo de Trabajo

<div align="center">

```mermaid
graph TD
    A[ðŸš€ Inicio] --> B[âš™ï¸ Configuración]
    B --> C[ðŸ§ª Prueba de Dispositivos]
    C --> D[ðŸŽ¯ selección de Fuentes]
    D --> E[ðŸŽ¤ grabación]
    E --> F[ðŸ“Š Procesamiento]
    F --> G[ðŸ”„ Mezcla Inteligente]
    G --> H[ðŸ“¦ Chunks AutomÃ¡ticos]
    H --> I[ðŸŒ EnvÃ­o Webhook]
    I --> J[ðŸ’¾ Almacenamiento Local]
    
    style A fill:#e1f5fe
    style E fill:#f3e5f5
    style J fill:#e8f5e8
```

</div>

---

## ðŸ—ï¸ ConstrucciÃ³n del Ejecutable

<details>
<summary>ðŸ› ï¸ <strong>Build Your Own</strong></summary>

### ðŸ“‹ Prerrequisitos
```bash
pip install PyInstaller
```

### ðŸš€ ConstrucciÃ³n
```bash
# ðŸ—ï¸ Construir ejecutable
python build.py

# ðŸ“¦ Crear paquete de distribuciÃ³n
python create_distribution.py
```

### ðŸ“ Resultado
```
dist/
â””â”€â”€ ðŸŽµ AudioCaptureWidget.exe  # âœ¨ Tu ejecutable listo
```

</details>

---

## ðŸ¤ Contribuir

<div align="center">

**ðŸŒŸ Â¡Las contribuciones son bienvenidas! ðŸŒŸ**

[![Contributors](https://img.shields.io/github/contributors/Pedroru101/audioAiV2?style=for-the-badge)](https://github.com/Pedroru101/audioAiV2/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/Pedroru101/audioAiV2?style=for-the-badge)](https://github.com/Pedroru101/audioAiV2/network/members)
[![Stars](https://img.shields.io/github/stars/Pedroru101/audioAiV2?style=for-the-badge)](https://github.com/Pedroru101/audioAiV2/stargazers)

</div>

### ðŸš€ CÃ³mo Contribuir

1. ðŸ´ **Fork** el proyecto
2. ðŸŒ¿ **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. ðŸ’¾ **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. ðŸ“¤ **Push** a la rama (`git push origin feature/AmazingFeature`)
5. ðŸ”„ **Abre** un Pull Request

### ðŸŽ¯ Ãreas de ContribuciÃ³n

<table>
<tr>
<td align="center">

**ðŸ› Bug Fixes**
- Reportar bugs
- Corregir errores
- Mejorar estabilidad

</td>
<td align="center">

**âœ¨ Features**
- Nuevas funcionalidades
- Mejoras de UI/UX
- Optimizaciones

</td>
<td align="center">

**ðŸ“š DocumentaciÃ³n**
- Mejorar README
- Tutoriales
- Ejemplos de uso

</td>
</tr>
</table>

---

## ðŸ“ Changelog

<details>
<summary>ðŸ“‹ <strong>Historial de Versiones</strong></summary>

### ðŸŽ‰ v1.0.0 (2024-07-22)
- âœ¨ **Nueva**: selección flexible de fuentes de grabación
- ðŸ§ª **Nueva**: Prueba independiente de dispositivos con reproducciÃ³n
- ðŸ”Š **Mejorado**: Soporte optimizado para VB-Audio Cable
- ðŸ“¦ **Nuevo**: Empaquetado en ejecutable standalone
- ðŸ§¹ **Mejorado**: Proyecto limpio y optimizado
- ðŸ“š **Nueva**: DocumentaciÃ³n completa y visual
- ðŸŽ¨ **Mejorado**: Interfaz mÃ¡s intuitiva y responsive
- ðŸ”§ **Nuevo**: Sistema de Configuración avanzado

</details>

---

## ðŸ› Problemas Conocidos

<div align="center">

### âš ï¸ Limitaciones Actuales

</div>

| Problema | DescripciÃ³n | SoluciÃ³n |
|----------|-------------|----------|
| ðŸ›¡ï¸ **Windows Defender** | Puede marcar el ejecutable como sospechoso | Falso positivo - Agregar excepciÃ³n |
| ðŸŽ¤ **Permisos de MicrÃ³fono** | Windows puede solicitar permisos | Permitir acceso la primera vez |
| ðŸ”Š **VB-Audio** | Requiere instalaciÃ³n separada | Descargar desde sitio oficial |

---

## ðŸ“„ Licencia

<div align="center">

**ðŸ“œ MIT License**

[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

*Este proyecto estÃ¡ bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles*

</div>

---

## ðŸ™ Agradecimientos

<div align="center">

### ðŸ’ Gracias a estas increÃ­bles tecnologÃ­as

</div>

<table>
<tr>
<td align="center">

**ðŸŽ¨ UI Framework**
[![PySide6](https://img.shields.io/badge/PySide6-41CD52?style=for-the-badge&logo=qt)](https://pypi.org/project/PySide6/)

</td>
<td align="center">

**ðŸŽµ Audio Engine**
[![sounddevice](https://img.shields.io/badge/sounddevice-FF6B6B?style=for-the-badge&logo=python)](https://pypi.org/project/sounddevice/)

</td>
<td align="center">

**ðŸ”Š Virtual Audio**
[![VB-Audio](https://img.shields.io/badge/VB--Audio-4ECDC4?style=for-the-badge)](https://vb-audio.com/)

</td>
<td align="center">

**ðŸ“¦ Packaging**
[![PyInstaller](https://img.shields.io/badge/PyInstaller-45B7D1?style=for-the-badge&logo=python)](https://pyinstaller.org/)

</td>
</tr>
</table>

---

## ðŸ“ž Soporte y Contacto

<div align="center">

### ðŸ†˜ Â¿Necesitas Ayuda?

[![Issues](https://img.shields.io/badge/ðŸ›_Reportar_Bug-Issues-red?style=for-the-badge)](https://github.com/Pedroru101/audioAiV2/issues)
[![Discussions](https://img.shields.io/badge/ðŸ’¬_Discusiones-Discussions-blue?style=for-the-badge)](https://github.com/Pedroru101/audioAiV2/discussions)
[![Email](https://img.shields.io/badge/ðŸ“§_Contacto-GitHub-green?style=for-the-badge)](https://github.com/Pedroru101)

</div>

### ðŸŽ¯ Canales de Soporte

- ðŸ› **Bugs**: [GitHub Issues](https://github.com/Pedroru101/audioAiV2/issues)
- ðŸ’¬ **Preguntas**: [GitHub Discussions](https://github.com/Pedroru101/audioAiV2/discussions)
- ðŸ“§ **Contacto**: A travÃ©s de GitHub
- ðŸ“š **Wiki**: DocumentaciÃ³n extendida (prÃ³ximamente)

---

<div align="center">

## ðŸŒŸ Â¡Dale una Estrella!

**Si te gusta este proyecto, Â¡no olvides darle una estrella!** â­

[![Star History Chart](https://api.star-history.com/svg?repos=Pedroru101/audioAiV2&type=Date)](https://star-history.com/#Pedroru101/audioAiV2&Date)

---

### ðŸŽµ **Desarrollado con â¤ï¸ para la comunidad de audio** ðŸŽµ

**ðŸš€ Audio Capture Widget - Donde la tecnologÃ­a se encuentra con la creatividad ðŸŽ¨**

---

*âš¡ Hecho con Python â€¢ ðŸŽ¨ DiseÃ±ado para Windows â€¢ ðŸŒŸ Open Source Forever*

</div>


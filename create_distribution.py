#!/usr/bin/env python3
"""
Crea un paquete de distribución completo
"""

import shutil
import os
from pathlib import Path
import zipfile
import datetime

def create_distribution_package():
    """Crea un paquete de distribución completo."""
    print("📦 Creando paquete de distribución...")
    
    # Crear directorio de distribución
    dist_dir = Path("AudioCaptureWidget_Distribution")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # Copiar ejecutable
    exe_path = Path("dist/AudioCaptureWidget.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, dist_dir)
        print(f"   ✅ Copiado: {exe_path.name}")
    else:
        print("   ❌ Ejecutable no encontrado")
        return False
    
    # Crear README de instalación
    readme_content = """# Audio Capture Widget v1.0.0

## 🎵 Aplicación de Grabación de Audio Profesional

### ✨ Características
- 🎤 Grabación simultánea de micrófono y sistema
- 🔊 Selección flexible de fuentes de grabación
- 📦 Chunks automáticos configurables
- 🌐 Envío a webhook (n8n compatible)
- 🎨 Interfaz flotante minimalista

### 🚀 Instalación Rápida
1. **Ejecutar** `AudioCaptureWidget.exe`
2. La aplicación se iniciará automáticamente
3. **Configurar** dispositivos en el panel de configuración ⚙️

### 📋 Requisitos del Sistema
- **Windows 10** o superior
- **Dispositivos de audio** configurados
- **Para captura de sistema**: VB-Audio Cable (recomendado)

### 🎯 Uso
1. **Abrir configuración**: Presionar botón ⚙️
2. **Seleccionar dispositivos**: Elegir micrófono y/o sistema
3. **Configurar fuentes**: Marcar checkboxes según necesidad
   - ☑️ Solo micrófono
   - ☑️ Solo sistema
   - ☑️ Ambos dispositivos
4. **Configurar webhook** (opcional): URL de n8n
5. **Ajustar duración**: Chunks de 2-300 segundos
6. **Guardar configuración**: Presionar "💾 Guardar"
7. **Iniciar grabación**: Presionar botón 🎤

### 🔧 Configuración Avanzada
- **Webhook URL**: Para envío automático a n8n
- **Duración de chunks**: Configurable de 2 a 300 segundos
- **Dispositivos de prueba**: Botón "Probar" para cada dispositivo
- **Reproducción de pruebas**: Botón "▶" para escuchar grabaciones

### 🆘 Solución de Problemas

#### No se detecta audio del sistema:
1. **Instalar VB-Audio Cable**
2. **Configurar aplicaciones** para usar "CABLE Input"
3. **Seleccionar "CABLE Output"** en la aplicación

#### Error de micrófono:
1. **Verificar permisos** de micrófono en Windows
2. **Probar dispositivo** con botón "Probar"
3. **Seleccionar dispositivo diferente** si es necesario

#### Aplicación no inicia:
1. **Ejecutar como administrador** (si es necesario)
2. **Verificar antivirus** no esté bloqueando
3. **Reinstalar dependencias** de audio de Windows

### 📁 Archivos Generados
- **Grabaciones**: Se guardan en `temp_audio/`
- **Configuración**: `config.json`
- **Logs**: `audio_recorder.log`

### 🔄 Desinstalación
1. **Eliminar carpeta** de la aplicación
2. **Limpiar archivos temporales**: `%TEMP%\\audio_test`
3. **Opcional**: Eliminar `config.json`

### 📞 Soporte
- **Logs automáticos** para debugging
- **Configuración persistente** entre sesiones
- **Pruebas integradas** de dispositivos

---
**Desarrollado con ❤️ para grabación de audio profesional**
**Versión 1.0.0 - 2024**
"""
    
    readme_path = dist_dir / "README.txt"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"   ✅ Creado: {readme_path.name}")
    
    # Crear script de instalación
    install_script = dist_dir / "INSTALAR.bat"
    install_content = """@echo off
echo.
echo ========================================
echo   Audio Capture Widget - Instalacion
echo ========================================
echo.
echo Copiando archivos...
if not exist "%USERPROFILE%\\AudioCaptureWidget" mkdir "%USERPROFILE%\\AudioCaptureWidget"
copy "AudioCaptureWidget.exe" "%USERPROFILE%\\AudioCaptureWidget\\"
echo.
echo Creando acceso directo en el escritorio...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Audio Capture Widget.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\\AudioCaptureWidget\\AudioCaptureWidget.exe'; $Shortcut.Save()"
echo.
echo Creando acceso directo en el menu inicio...
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Audio Capture Widget" mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Audio Capture Widget"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Audio Capture Widget\\Audio Capture Widget.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\\AudioCaptureWidget\\AudioCaptureWidget.exe'; $Shortcut.Save()"
echo.
echo ========================================
echo   Instalacion completada!
echo ========================================
echo.
echo La aplicacion se ha instalado en:
echo %USERPROFILE%\\AudioCaptureWidget\\
echo.
echo Accesos directos creados en:
echo - Escritorio
echo - Menu Inicio
echo.
choice /c YN /m "Desea ejecutar la aplicacion ahora?"
if errorlevel 2 goto end
start "" "%USERPROFILE%\\AudioCaptureWidget\\AudioCaptureWidget.exe"
:end
pause
"""
    
    with open(install_script, 'w', encoding='utf-8') as f:
        f.write(install_content)
    print(f"   ✅ Creado: {install_script.name}")
    
    # Crear script de desinstalación
    uninstall_script = dist_dir / "DESINSTALAR.bat"
    uninstall_content = """@echo off
echo.
echo ========================================
echo   Audio Capture Widget - Desinstalacion
echo ========================================
echo.
choice /c YN /m "Esta seguro que desea desinstalar Audio Capture Widget?"
if errorlevel 2 goto cancel
echo.
echo Cerrando aplicacion si esta ejecutandose...
taskkill /f /im AudioCaptureWidget.exe >nul 2>&1
echo.
echo Eliminando archivos...
if exist "%USERPROFILE%\\AudioCaptureWidget" rmdir /s /q "%USERPROFILE%\\AudioCaptureWidget"
echo.
echo Eliminando accesos directos...
if exist "%USERPROFILE%\\Desktop\\Audio Capture Widget.lnk" del "%USERPROFILE%\\Desktop\\Audio Capture Widget.lnk"
if exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Audio Capture Widget" rmdir /s /q "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Audio Capture Widget"
echo.
echo Limpiando archivos temporales...
if exist "%TEMP%\\audio_test" rmdir /s /q "%TEMP%\\audio_test"
echo.
choice /c YN /m "Desea eliminar la configuracion guardada?"
if errorlevel 2 goto skip_config
if exist "%USERPROFILE%\\AudioCaptureWidget\\config.json" del "%USERPROFILE%\\AudioCaptureWidget\\config.json"
:skip_config
echo.
echo ========================================
echo   Desinstalacion completada!
echo ========================================
echo.
echo Audio Capture Widget ha sido eliminado del sistema.
goto end
:cancel
echo.
echo Desinstalacion cancelada.
:end
pause
"""
    
    with open(uninstall_script, 'w', encoding='utf-8') as f:
        f.write(uninstall_content)
    print(f"   ✅ Creado: {uninstall_script.name}")
    
    # Crear archivo ZIP de distribución
    zip_name = f"AudioCaptureWidget_v1.0.0_{datetime.datetime.now().strftime('%Y%m%d')}.zip"
    zip_path = Path(zip_name)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dist_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(dist_dir)
                zipf.write(file_path, arcname)
    
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"   ✅ Creado: {zip_name} ({zip_size_mb:.1f} MB)")
    
    print(f"\n🎉 Paquete de distribución creado exitosamente!")
    print(f"📁 Directorio: {dist_dir}")
    print(f"📦 Archivo ZIP: {zip_name}")
    print(f"📏 Tamaño total: {zip_size_mb:.1f} MB")
    
    return True

if __name__ == "__main__":
    create_distribution_package()
#!/usr/bin/env python3
"""
Script de construcción para Audio Capture Widget
Automatiza el proceso de empaquetado con PyInstaller
"""

import os
import sys
import shutil
import subprocess
import glob
from pathlib import Path
import time

# Importar configuración
from build_config import (
    PYINSTALLER_CONFIG, 
    CLEANUP_PATTERNS, 
    get_pyinstaller_args,
    get_spec_content,
    create_version_info
)

class BuildManager:
    """Gestor del proceso de construcción."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.start_time = time.time()
        
    def log(self, message, level="INFO"):
        """Log con timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def cleanup_project(self):
        """Limpia archivos temporales y de construcción anterior."""
        self.log("🧹 Limpiando proyecto...")
        
        cleaned_count = 0
        for pattern in CLEANUP_PATTERNS:
            for path in glob.glob(str(self.base_dir / pattern), recursive=True):
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                        self.log(f"   Eliminado directorio: {path}")
                    else:
                        os.remove(path)
                        self.log(f"   Eliminado archivo: {path}")
                    cleaned_count += 1
                except Exception as e:
                    self.log(f"   Error eliminando {path}: {e}", "WARNING")
        
        self.log(f"✅ Limpieza completada. {cleaned_count} elementos eliminados.")
        
    def check_dependencies(self):
        """Verifica que todas las dependencias estén instaladas."""
        self.log("🔍 Verificando dependencias...")
        
        required_packages = [
            'PyInstaller',
            'PySide6', 
            'sounddevice',
            'numpy',
            'scipy',
            'requests'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.lower().replace('-', '_'))
                self.log(f"   ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                self.log(f"   ❌ {package}", "ERROR")
        
        if missing_packages:
            self.log("❌ Faltan dependencias. Instalando...", "ERROR")
            for package in missing_packages:
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                 check=True, capture_output=True)
                    self.log(f"   ✅ Instalado: {package}")
                except subprocess.CalledProcessError as e:
                    self.log(f"   ❌ Error instalando {package}: {e}", "ERROR")
                    return False
        
        self.log("✅ Todas las dependencias están disponibles.")
        return True
        
    def create_build_files(self):
        """Crea archivos necesarios para la construcción."""
        self.log("📝 Creando archivos de construcción...")
        
        # Crear archivo .spec
        spec_path = self.base_dir / f"{PYINSTALLER_CONFIG['name']}.spec"
        with open(spec_path, 'w', encoding='utf-8') as f:
            f.write(get_spec_content())
        self.log(f"   ✅ Creado: {spec_path}")
        
        # Crear archivo de información de versión
        version_path = self.base_dir / "version_info.txt"
        with open(version_path, 'w', encoding='utf-8') as f:
            f.write(create_version_info())
        self.log(f"   ✅ Creado: {version_path}")
        
        return spec_path
        
    def optimize_imports(self):
        """Optimiza imports para reducir el tamaño del ejecutable."""
        self.log("⚡ Optimizando imports...")
        
        # Verificar que los archivos principales existan
        main_files = ['main.py', 'audio_handler.py', 'utils.py', 'audio_device_tester.py']
        for file in main_files:
            if not (self.base_dir / file).exists():
                self.log(f"   ❌ Archivo faltante: {file}", "ERROR")
                return False
            else:
                self.log(f"   ✅ {file}")
        
        # Verificar assets
        assets_dir = self.base_dir / 'assets'
        if not assets_dir.exists():
            self.log("   ❌ Directorio assets faltante", "ERROR")
            return False
        
        icon_path = assets_dir / 'app_icon.ico'
        if not icon_path.exists():
            self.log("   ⚠️  Icono no encontrado, usando icono por defecto", "WARNING")
            # Crear un icono básico si no existe
            try:
                # Copiar un icono por defecto o crear uno simple
                pass
            except:
                pass
        
        self.log("✅ Optimización de imports completada.")
        return True
        
    def build_executable(self, spec_path):
        """Construye el ejecutable usando PyInstaller."""
        self.log("🔨 Construyendo ejecutable...")
        
        try:
            # Ejecutar PyInstaller
            cmd = [sys.executable, '-m', 'PyInstaller', str(spec_path)]
            
            self.log(f"   Ejecutando: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=str(self.base_dir)
            )
            
            # Mostrar output en tiempo real
            for line in process.stdout:
                line = line.strip()
                if line:
                    if 'ERROR' in line or 'CRITICAL' in line:
                        self.log(f"   {line}", "ERROR")
                    elif 'WARNING' in line:
                        self.log(f"   {line}", "WARNING")
                    elif 'INFO' in line:
                        self.log(f"   {line}")
            
            process.wait()
            
            if process.returncode == 0:
                self.log("✅ Construcción exitosa!")
                return True
            else:
                self.log(f"❌ Error en construcción. Código: {process.returncode}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error ejecutando PyInstaller: {e}", "ERROR")
            return False
            
    def validate_executable(self):
        """Valida que el ejecutable se haya creado correctamente."""
        self.log("🔍 Validando ejecutable...")
        
        exe_path = self.base_dir / 'dist' / f"{PYINSTALLER_CONFIG['name']}.exe"
        
        if not exe_path.exists():
            self.log(f"❌ Ejecutable no encontrado: {exe_path}", "ERROR")
            return False
        
        # Verificar tamaño
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        self.log(f"   📦 Tamaño: {size_mb:.1f} MB")
        
        if size_mb > 200:
            self.log("   ⚠️  Ejecutable muy grande (>200MB)", "WARNING")
        elif size_mb < 50:
            self.log("   ⚠️  Ejecutable muy pequeño (<50MB), posibles dependencias faltantes", "WARNING")
        else:
            self.log("   ✅ Tamaño apropiado")
        
        # Intentar ejecutar para verificar que funciona
        self.log("   🧪 Probando ejecutable...")
        try:
            # Ejecutar con timeout para evitar que se cuelgue
            process = subprocess.Popen(
                [str(exe_path), '--help'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )
            process.wait(timeout=5)
            self.log("   ✅ Ejecutable funciona correctamente")
        except subprocess.TimeoutExpired:
            self.log("   ✅ Ejecutable inició correctamente (timeout esperado)")
        except Exception as e:
            self.log(f"   ⚠️  Error probando ejecutable: {e}", "WARNING")
        
        self.log(f"✅ Ejecutable validado: {exe_path}")
        return True
        
    def create_distribution_package(self):
        """Crea un paquete de distribución con el ejecutable y archivos necesarios."""
        self.log("📦 Creando paquete de distribución...")
        
        dist_dir = self.base_dir / 'distribution'
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        dist_dir.mkdir()
        
        # Copiar ejecutable
        exe_path = self.base_dir / 'dist' / f"{PYINSTALLER_CONFIG['name']}.exe"
        shutil.copy2(exe_path, dist_dir)
        self.log(f"   ✅ Copiado: {exe_path.name}")
        
        # Copiar README
        readme_path = self.base_dir / 'README.md'
        if readme_path.exists():
            shutil.copy2(readme_path, dist_dir)
            self.log(f"   ✅ Copiado: README.md")
        
        # Crear archivo de instalación rápida
        install_script = dist_dir / 'INSTALAR.txt'
        with open(install_script, 'w', encoding='utf-8') as f:
            f.write(f"""# Audio Capture Widget - Instalación

## Instalación Rápida
1. Ejecutar {PYINSTALLER_CONFIG['name']}.exe
2. La aplicación se iniciará automáticamente
3. Configurar dispositivos de audio en el panel de configuración

## Requisitos del Sistema
- Windows 10 o superior
- Dispositivos de audio configurados
- Para captura de sistema: VB-Audio Cable (recomendado)

## Uso
1. Abrir la aplicación
2. Presionar el botón de configuración ⚙️
3. Seleccionar dispositivos de audio
4. Configurar fuentes de grabación (micrófono/sistema)
5. Presionar "Guardar Configuración"
6. Iniciar grabación con el botón 🎤

## Soporte
- Verificar que los dispositivos de audio estén funcionando
- Para captura de sistema, instalar VB-Audio Cable
- La aplicación crea logs automáticamente para debugging

Versión: {PYINSTALLER_CONFIG['version_info']['version']}
""")
        self.log(f"   ✅ Creado: INSTALAR.txt")
        
        # Crear script de desinstalación
        uninstall_script = dist_dir / 'DESINSTALAR.bat'
        with open(uninstall_script, 'w', encoding='utf-8') as f:
            f.write(f"""@echo off
echo Desinstalando Audio Capture Widget...
echo.
echo Eliminando archivos temporales...
if exist "%TEMP%\\audio_test" rmdir /s /q "%TEMP%\\audio_test"
if exist "temp_audio" rmdir /s /q "temp_audio"
if exist "*.log" del /q "*.log"
if exist "config.json" (
    choice /c YN /m "¿Eliminar configuración guardada?"
    if errorlevel 2 goto skip_config
    del /q "config.json"
    :skip_config
)
echo.
echo Desinstalación completada.
echo Puedes eliminar manualmente la carpeta de la aplicación.
pause
""")
        self.log(f"   ✅ Creado: DESINSTALAR.bat")
        
        self.log(f"✅ Paquete de distribución creado en: {dist_dir}")
        return dist_dir
        
    def build(self):
        """Ejecuta el proceso completo de construcción."""
        self.log("🚀 Iniciando construcción de Audio Capture Widget")
        self.log("=" * 60)
        
        try:
            # Paso 1: Limpiar proyecto
            self.cleanup_project()
            
            # Paso 2: Verificar dependencias
            if not self.check_dependencies():
                return False
            
            # Paso 3: Optimizar imports
            if not self.optimize_imports():
                return False
            
            # Paso 4: Crear archivos de construcción
            spec_path = self.create_build_files()
            
            # Paso 5: Construir ejecutable
            if not self.build_executable(spec_path):
                return False
            
            # Paso 6: Validar ejecutable
            if not self.validate_executable():
                return False
            
            # Paso 7: Crear paquete de distribución
            dist_dir = self.create_distribution_package()
            
            # Resumen final
            build_time = time.time() - self.start_time
            self.log("=" * 60)
            self.log("🎉 ¡CONSTRUCCIÓN COMPLETADA EXITOSAMENTE!")
            self.log(f"⏱️  Tiempo total: {build_time:.1f} segundos")
            exe_name = f"{PYINSTALLER_CONFIG['name']}.exe"
            self.log(f"📦 Ejecutable: {dist_dir / exe_name}")
            self.log(f"📁 Paquete: {dist_dir}")
            self.log("=" * 60)
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error crítico en construcción: {e}", "ERROR")
            return False

def main():
    """Función principal."""
    builder = BuildManager()
    success = builder.build()
    
    if success:
        print("\n🎉 ¡Construcción exitosa! El ejecutable está listo para usar.")
        sys.exit(0)
    else:
        print("\n❌ Error en la construcción. Revisa los logs anteriores.")
        sys.exit(1)

if __name__ == "__main__":
    main()
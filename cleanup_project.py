#!/usr/bin/env python3
"""
Script de limpieza del proyecto Audio Capture Widget
Elimina archivos temporales, de construcción y innecesarios
"""

import os
import shutil
import glob
from pathlib import Path
import time

class ProjectCleaner:
    """Limpiador del proyecto."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.cleaned_files = []
        self.cleaned_dirs = []
        self.preserved_files = []
        
    def log(self, message, level="INFO"):
        """Log con timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def get_cleanup_patterns(self):
        """Define patrones de archivos y directorios a limpiar."""
        return {
            # Archivos temporales de Python
            'python_temp': [
                '**/__pycache__',
                '**/*.pyc',
                '**/*.pyo',
                '**/*.pyd',
                '**/.pytest_cache',
            ],
            
            # Archivos de construcción PyInstaller
            'build_files': [
                'build/',
                'dist/',
                '*.spec',
                'version_info.txt',
            ],
            
            # Archivos temporales de audio
            'audio_temp': [
                'temp_audio/',
                '**/audio_test/',
                '**/*.log',
                'audio_recorder.log',
            ],
            
            # Archivos de desarrollo y testing
            'dev_files': [
                'test_*.py',
                '*_test.py',
                'debug_*.py',
                'temp_*.py',
                'backup_*.py',
            ],
            
            # Archivos de distribución generados
            'distribution': [
                'AudioCaptureWidget_Distribution/',
                'AudioCaptureWidget_v*.zip',
                'distribution/',
            ],
            
            # Archivos de configuración temporal
            'temp_config': [
                'config_temp.json',
                'config_backup.json',
                '*.tmp',
                '*.bak',
            ],
            
            # Archivos del sistema
            'system_files': [
                '.DS_Store',
                'Thumbs.db',
                'desktop.ini',
                '*.swp',
                '*.swo',
                '*~',
            ],
            
            # Scripts de construcción (mantener solo el principal)
            'build_scripts': [
                'build_config.py',
                'build_robust.py',
                'test_exe.py',
                'AudioCaptureWidget_simple.spec',
                'AudioCaptureWidget_robust.spec',
            ]
        }
    
    def get_essential_files(self):
        """Define archivos esenciales que NO deben eliminarse."""
        return {
            # Código fuente principal
            'main.py',
            'audio_handler.py', 
            'utils.py',
            'audio_device_tester.py',
            
            # Configuración
            'config.json',
            'requirements.txt',
            
            # Documentación
            'README.md',
            
            # Assets
            'assets/',
            
            # Scripts de construcción esenciales
            'build.py',
            'create_distribution.py',
            'cleanup_project.py',
            
            # Git
            '.git/',
            '.gitignore',
            
            # Kiro specs (si existen)
            '.kiro/',
        }
    
    def scan_for_cleanup(self):
        """Escanea el proyecto para identificar archivos a limpiar."""
        self.log("🔍 Escaneando proyecto para limpieza...")
        
        cleanup_patterns = self.get_cleanup_patterns()
        essential_files = self.get_essential_files()
        
        files_to_clean = []
        
        for category, patterns in cleanup_patterns.items():
            self.log(f"   Escaneando categoría: {category}")
            
            for pattern in patterns:
                matches = list(self.base_dir.glob(pattern))
                for match in matches:
                    # Verificar que no sea un archivo esencial
                    relative_path = match.relative_to(self.base_dir)
                    if not any(str(relative_path).startswith(essential) for essential in essential_files):
                        files_to_clean.append((match, category))
                        
        return files_to_clean
    
    def clean_files(self, files_to_clean, dry_run=False):
        """Limpia los archivos identificados."""
        if dry_run:
            self.log("🧪 MODO SIMULACIÓN - No se eliminarán archivos realmente")
        else:
            self.log("🧹 Iniciando limpieza de archivos...")
        
        cleaned_count = 0
        total_size = 0
        
        for file_path, category in files_to_clean:
            try:
                if file_path.exists():
                    # Calcular tamaño
                    if file_path.is_file():
                        size = file_path.stat().st_size
                        total_size += size
                    elif file_path.is_dir():
                        size = sum(f.stat().st_size for f in file_path.rglob('*') if f.is_file())
                        total_size += size
                    
                    size_mb = size / (1024 * 1024)
                    
                    if not dry_run:
                        if file_path.is_dir():
                            shutil.rmtree(file_path)
                            self.cleaned_dirs.append(str(file_path))
                            self.log(f"   🗂️  Eliminado directorio: {file_path} ({size_mb:.2f} MB) [{category}]")
                        else:
                            file_path.unlink()
                            self.cleaned_files.append(str(file_path))
                            self.log(f"   📄 Eliminado archivo: {file_path} ({size_mb:.2f} MB) [{category}]")
                    else:
                        file_type = "directorio" if file_path.is_dir() else "archivo"
                        self.log(f"   🔍 Se eliminaría {file_type}: {file_path} ({size_mb:.2f} MB) [{category}]")
                    
                    cleaned_count += 1
                    
            except Exception as e:
                self.log(f"   ❌ Error procesando {file_path}: {e}", "ERROR")
        
        total_size_mb = total_size / (1024 * 1024)
        
        if dry_run:
            self.log(f"📊 SIMULACIÓN: Se eliminarían {cleaned_count} elementos ({total_size_mb:.2f} MB)")
        else:
            self.log(f"✅ Limpieza completada: {cleaned_count} elementos eliminados ({total_size_mb:.2f} MB)")
        
        return cleaned_count, total_size_mb
    
    def create_gitignore(self):
        """Crea o actualiza .gitignore para evitar archivos innecesarios."""
        self.log("📝 Actualizando .gitignore...")
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Audio files temporales
temp_audio/
audio_test/
*.log

# Configuración temporal
config_temp.json
config_backup.json
*.tmp
*.bak

# Distribución
AudioCaptureWidget_Distribution/
AudioCaptureWidget_v*.zip
distribution/

# Sistema
.DS_Store
Thumbs.db
desktop.ini
*.swp
*.swo
*~

# IDE
.vscode/
.idea/
*.sublime-*

# Testing
.pytest_cache/
.coverage
htmlcov/

# Entornos virtuales
venv/
env/
ENV/
"""
        
        gitignore_path = self.base_dir / '.gitignore'
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        self.log(f"   ✅ Actualizado: {gitignore_path}")
    
    def show_project_structure(self):
        """Muestra la estructura final del proyecto."""
        self.log("📁 Estructura final del proyecto:")
        
        def show_tree(path, prefix="", max_depth=3, current_depth=0):
            if current_depth >= max_depth:
                return
                
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                
                if item.name.startswith('.') and item.name not in ['.git', '.gitignore', '.kiro']:
                    continue
                    
                print(f"{prefix}{current_prefix}{item.name}")
                
                if item.is_dir() and not item.name.startswith('.'):
                    extension = "    " if is_last else "│   "
                    show_tree(item, prefix + extension, max_depth, current_depth + 1)
        
        show_tree(self.base_dir)
    
    def create_cleanup_report(self):
        """Crea un reporte de la limpieza realizada."""
        report_content = f"""# Reporte de Limpieza del Proyecto
Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}

## Archivos Eliminados ({len(self.cleaned_files)})
"""
        
        for file_path in self.cleaned_files:
            report_content += f"- {file_path}\n"
        
        report_content += f"\n## Directorios Eliminados ({len(self.cleaned_dirs)})\n"
        
        for dir_path in self.cleaned_dirs:
            report_content += f"- {dir_path}/\n"
        
        report_content += f"""
## Archivos Preservados
Los siguientes archivos esenciales se mantuvieron:
- main.py (aplicación principal)
- audio_handler.py (motor de grabación)
- utils.py (utilidades)
- audio_device_tester.py (prueba de dispositivos)
- config.json (configuración)
- requirements.txt (dependencias)
- README.md (documentación)
- assets/ (recursos)
- build.py (script de construcción)
- create_distribution.py (script de distribución)

## Recomendaciones
1. Ejecutar 'git status' para verificar cambios
2. Probar que la aplicación funcione correctamente
3. Crear nuevo ejecutable si es necesario
4. El .gitignore ha sido actualizado para evitar archivos innecesarios
"""
        
        report_path = self.base_dir / 'cleanup_report.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.log(f"📄 Reporte creado: {report_path}")
    
    def cleanup(self, dry_run=False):
        """Ejecuta la limpieza completa del proyecto."""
        self.log("🚀 Iniciando limpieza del proyecto Audio Capture Widget")
        self.log("=" * 60)
        
        # Paso 1: Escanear archivos
        files_to_clean = self.scan_for_cleanup()
        
        if not files_to_clean:
            self.log("✨ El proyecto ya está limpio - no hay archivos para eliminar")
            return True
        
        # Paso 2: Mostrar lo que se va a limpiar
        self.log(f"📋 Se encontraron {len(files_to_clean)} elementos para limpiar")
        
        # Paso 3: Limpiar archivos
        cleaned_count, total_size_mb = self.clean_files(files_to_clean, dry_run)
        
        if not dry_run:
            # Paso 4: Actualizar .gitignore
            self.create_gitignore()
            
            # Paso 5: Crear reporte
            self.create_cleanup_report()
            
            # Paso 6: Mostrar estructura final
            self.show_project_structure()
            
            self.log("=" * 60)
            self.log("🎉 ¡Limpieza completada exitosamente!")
            self.log(f"📊 Elementos eliminados: {cleaned_count}")
            self.log(f"💾 Espacio liberado: {total_size_mb:.2f} MB")
            self.log("📄 Ver cleanup_report.txt para detalles completos")
        
        return True

def main():
    """Función principal."""
    import sys
    
    # Verificar argumentos
    dry_run = '--dry-run' in sys.argv or '--simulate' in sys.argv
    
    if dry_run:
        print("🧪 Ejecutando en modo SIMULACIÓN")
        print("   Use sin --dry-run para ejecutar la limpieza real")
        print()
    
    cleaner = ProjectCleaner()
    success = cleaner.cleanup(dry_run=dry_run)
    
    if success:
        if not dry_run:
            print("\n✅ Limpieza completada. El proyecto está listo para distribución.")
        else:
            print("\n🔍 Simulación completada. Use sin --dry-run para limpiar realmente.")
        sys.exit(0)
    else:
        print("\n❌ Error en la limpieza.")
        sys.exit(1)

if __name__ == "__main__":
    main()
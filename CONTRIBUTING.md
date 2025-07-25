# 🤝 Contribuir a Audio Capture Widget

¡Gracias por tu interés en contribuir al proyecto! Este documento te guiará sobre cómo participar de manera efectiva.

## 🎯 Cómo Contribuir

### 🐛 Reportar Bugs
- Usa [GitHub Issues](https://github.com/Pedroru101/audioAiV2/issues)
- Incluye pasos para reproducir el problema
- Especifica tu versión de Windows y Python
- Adjunta logs si es posible

### 💡 Sugerir Features
- Usa [GitHub Discussions](https://github.com/Pedroru101/audioAiV2/discussions)
- Describe el caso de uso específico
- Explica cómo beneficiaría a otros usuarios

### 🔧 Pull Requests
1. **Fork** el repositorio
2. **Crea una rama** para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. **Haz tus cambios** siguiendo las convenciones del código
4. **Prueba** tu código localmente
5. **Commit** con mensajes descriptivos
6. **Push** a tu fork: `git push origin feature/nueva-funcionalidad`
7. **Abre un Pull Request** con descripción detallada

## 📋 Proceso de Review

### ✅ Criterios de Aceptación
- ✅ El código sigue las convenciones existentes
- ✅ Incluye pruebas si es aplicable
- ✅ No rompe funcionalidad existente
- ✅ Documentación actualizada si es necesario
- ✅ Commit messages claros y descriptivos

### 🔍 Review Process
1. **Automático**: GitHub Actions ejecuta tests
2. **Manual**: @Pedroru101 revisa el código
3. **Feedback**: Se proporcionan comentarios si es necesario
4. **Merge**: Una vez aprobado, se integra a main

## 🎨 Convenciones de Código

### 🐍 Python Style
- Sigue PEP 8
- Usa type hints cuando sea posible
- Documenta funciones complejas
- Mantén líneas bajo 100 caracteres

### 📝 Commit Messages
```
tipo(scope): descripción breve

Descripción más detallada si es necesario

- Cambio específico 1
- Cambio específico 2
```

**Tipos:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato
- `refactor`: Refactoring de código
- `test`: Agregar o modificar tests

## 🚀 Setup de Desarrollo

### 📦 Instalación
```bash
git clone https://github.com/TU_USERNAME/audioAiV2.git
cd audioAiV2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 🧪 Testing
```bash
python -m pytest tests/
python main.py  # Test manual
```

### 🏗️ Build
```bash
python build.py  # Crear ejecutable
```

## 🤖 Integración con n8n

### 📋 Testing de Workflows
- Usa n8n local para pruebas
- Documenta configuraciones específicas
- Incluye ejemplos de payloads
- Prueba con diferentes servicios de IA

### 🧠 LLM Integration
- Testa con múltiples proveedores (OpenAI, Anthropic, etc.)
- Valida formatos de audio compatibles
- Documenta limitaciones conocidas

## 📞 Contacto

- 🐛 **Issues**: [GitHub Issues](https://github.com/Pedroru101/audioAiV2/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Pedroru101/audioAiV2/discussions)
- 📧 **Maintainer**: @Pedroru101

## 📄 Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la misma [MIT License](LICENSE) del proyecto.

---

**🎵 ¡Gracias por ayudar a mejorar Audio Capture Widget! 🎵**
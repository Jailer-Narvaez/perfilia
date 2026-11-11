# Constitution – Perfilia

## 1. Objetivo del proyecto

Desarrollar un bot de Telegram que adapte currículums a ofertas laborales utilizando modelos de lenguaje, manteniendo siempre la veracidad de la información profesional del usuario.

## 2. Principios de desarrollo

- **Simplicidad:** implementar soluciones sencillas, evitando complejidad innecesaria.
- **Modularidad:** mantener separadas las responsabilidades de cada componente.
- **Mantenibilidad:** escribir código claro, organizado y fácil de modificar.
- **Configuración:** evitar credenciales y valores sensibles directamente en el código.
- **Escalabilidad:** permitir incorporar nuevas funcionalidades sin tener que reconstruir el proyecto.

## 3. Reglas obligatorias

### Integridad de la información

- El archivo `cv_base.md` es la fuente principal de información profesional.
- Nunca inventar experiencia, habilidades, estudios, certificaciones, cargos, fechas o logros.
- La adaptación puede cambiar la redacción y organización, pero no alterar los hechos.
- La validación del contenido es obligatoria antes de generar cualquier PDF.
- La información no respaldada debe auto-corregirse en bucle; si no puede eliminarse, no se debe entregar el documento.
- El PDF solo se genera cuando el cumplimiento con la oferta es igual o superior al umbral configurado (por defecto 70 %).
- El CV base solo se modifica para agregar información (skills, educación o experiencia) con confirmación explícita del usuario, nunca de forma automática.

### Uso del LLM

- Los prompts deben estar escritos en inglés.
- El idioma de respuesta debe ser configurable.
- El proveedor LLM debe poder cambiarse mediante configuración.
- No depender de un único proveedor para el funcionamiento futuro del proyecto.

### Generación de documentos

- Los PDF deben tener un diseño profesional, sobrio y de una sola columna.
- Priorizar la compatibilidad con sistemas ATS.
- No incluir elementos visuales que dificulten la lectura automática del documento.

### Almacenamiento

- Cada adaptación debe registrarse de forma independiente.
- No modificar el CV base durante el proceso de adaptación.
- Mantener los documentos generados organizados y asociados a su registro histórico.

## 4. Calidad del código

- Utilizar Python 3.13 o superior.
- Seguir convenciones PEP 8.
- Utilizar nombres descriptivos para variables, funciones y clases.
- Evitar duplicar código.
- Manejar explícitamente los errores de Telegram, extracción de ofertas, LLM, validación y generación de PDF.
- Mantener las dependencias y configuraciones documentadas.

## 5. Seguridad

- No subir archivos `.env` ni credenciales al repositorio.
- Validar las URLs recibidas antes de procesarlas.
- Limitar el contenido externo que se descarga.
- No ejecutar instrucciones ni código obtenido desde ofertas laborales o respuestas del LLM.
- Evitar exponer información personal del CV en registros innecesarios.

## 6. Documentación

- Mantener actualizados `architecture.md`, `features.md` y `constitution.md`.
- Documentar únicamente decisiones relevantes para el desarrollo.
- Evitar documentación extensa o innecesariamente técnica.
- Actualizar la documentación cuando cambie el comportamiento del sistema.

## 7. Criterio para nuevas funcionalidades

Toda nueva funcionalidad debe cumplir estas condiciones:

1. Aportar valor al objetivo principal del proyecto.
2. Respetar la integridad de la información del usuario.
3. Mantener la simplicidad del sistema.
4. No comprometer las funcionalidades existentes.

**Regla principal:** la calidad de un CV adaptado nunca debe estar por encima de la veracidad de su contenido.
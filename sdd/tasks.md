# Tasks – Perfilia

## Fase 1. Configuración inicial

- [x] Crear la estructura de carpetas del proyecto.
- [x] Configurar el entorno virtual de Python.
- [x] Crear `requirements.txt` con las dependencias.
- [x] Configurar las variables de entorno mediante `.env`.
- [x] Crear `main.py` como punto de entrada.
- [x] Configurar el sistema de logs y manejo de errores.

## Fase 2. Bot de Telegram

- [x] Crear y configurar el bot de Telegram.
- [x] Implementar la recepción de mensajes.
- [x] Crear el comando `/start`.
- [x] Implementar la recepción de enlaces de ofertas laborales.
- [x] Implementar la recepción de texto de ofertas laborales.
- [x] Permitir enviar documentos PDF al usuario.

## Fase 3. Gestión de ofertas laborales

- [x] Implementar la extracción de contenido desde URLs.
- [x] Validar las URLs recibidas.
- [x] Solicitar el texto manualmente cuando falle la extracción.
- [x] Preparar el contenido de la oferta para el análisis.

## Fase 4. Integración con LLM

- [x] Configurar la conexión con Gemini mediante freelm.
- [x] Crear los prompts para analizar ofertas laborales.
- [x] Implementar la lectura del CV desde `cv_base.md`.
- [x] Crear el prompt para adaptar el CV.
- [x] Permitir configurar el idioma de salida.
- [x] Implementar el proceso completo de adaptación.
- [x] Manejar errores y respuestas inválidas del proveedor.

## Fase 5. Validación del CV

- [x] Crear el mecanismo de validación del contenido generado.
- [x] Comparar la información con el CV original.
- [x] Detectar información no respaldada por el CV base.
- [x] Auto-corregir el CV adaptado en bucle hasta eliminar la información no respaldada.
- [x] Evaluar el porcentaje de cumplimiento del CV con respecto a la oferta.
- [x] Bloquear la generación del PDF cuando la fidelidad falle o no se alcance el umbral.
- [x] Informar al usuario el porcentaje y las brechas principales.
- [x] Consultar por los conocimientos o experiencia faltantes y completar el CV con la respuesta en texto libre.

## Fase 6. Generación del PDF

- [x] Crear la plantilla del currículum (layout programático con fpdf2).
- [x] Aplicar un diseño sobrio de una columna y compatible con ATS.
- [x] Implementar la conversión a PDF con fpdf2.
- [x] Guardar los documentos generados.
- [x] Enviar el PDF mediante Telegram.

## Fase 7. Historial

- [x] Configurar SQLite.
- [x] Crear la estructura de almacenamiento de adaptaciones.
- [x] Registrar las ofertas laborales procesadas.
- [x] Guardar el contenido de los CV adaptados.
- [x] Asociar cada registro con su PDF generado.
- [x] Implementar la consulta del historial (comando `/historial`).
- [x] Persistir la fuente de la oferta (URL o texto).
- [x] Solicitar al usuario el origen de la oferta dentro del flujo.
- [x] Permitir eliminar registros del historial mediante `/eliminar <id>`.

## Fase 8. Pruebas y finalización

- [ ] Probar la recepción de ofertas mediante texto.
- [ ] Probar la extracción de ofertas mediante URL.
- [ ] Probar la adaptación del CV.
- [ ] Verificar que no se genere información inventada.
- [ ] Probar el bloqueo del PDF cuando falle la validación.
- [ ] Verificar la generación y entrega del PDF.
- [ ] Verificar el almacenamiento del historial.
- [ ] Actualizar la documentación del proyecto.

---

## Mejoras futuras

- [ ] Incorporar nuevos proveedores LLM.
- [ ] Implementar soporte multiusuario.
- [ ] Incorporar Webhook para despliegue en VPS.
- [ ] Agregar exportación a DOCX.
- [ ] Migrar de SQLite a PostgreSQL si el crecimiento del proyecto lo requiere.
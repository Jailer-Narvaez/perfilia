# Features – Perfilia

## 1. Gestión del CV base

- Leer el CV original desde `cv_base.md`.
- Utilizarlo como única fuente de información profesional.
- Permitir actualizar el archivo para mantener la información vigente.
- Permitir agregar información confirmada por el usuario cuando falten requisitos de la oferta (skills, educación o experiencia).

## 2. Recepción de ofertas laborales

- Recibir ofertas mediante enlaces o texto enviado por Telegram.
- Extraer automáticamente el contenido de una URL.
- Si no es posible extraer la información, solicitar al usuario que envíe el texto de la oferta.
- Identificar los requisitos, habilidades y responsabilidades del cargo.
- Solicitar al usuario el origen o fuente de la oferta para registrarla en el historial.

## 3. Adaptación del CV

- Analizar la oferta laboral y compararla con el CV base.
- Adaptar el perfil profesional, habilidades y experiencia para destacar la información más relevante.
- Utilizar palabras clave relacionadas con la oferta.
- Mantener la información original sin inventar experiencia o conocimientos.
- Generar el resultado en español por defecto, con posibilidad de configurar otro idioma.

## 4. Validación de contenido

- Comparar el CV generado con la información del CV base.
- Detectar información inventada, modificada o no respaldada.
- Auto-corregir el CV adaptado en bucle hasta eliminar la información no respaldada.
- Evaluar el porcentaje de cumplimiento del CV base con respecto a la oferta.
- Generar el PDF únicamente si el cumplimiento es igual o superior al umbral configurado (por defecto 70 %).
- Informar al usuario el porcentaje obtenido y, en caso de no alcanzarlo, las brechas principales.
- Consultar al usuario por los conocimientos o experiencia faltantes; con la respuesta en texto libre, el modelo razona y completa el CV en la sección correspondiente, y se re-evalúa.
- Impedir la generación del PDF cuando no sea posible validar el contenido.

## 5. Generación del PDF

- Convertir el CV adaptado a PDF mediante fpdf2.
- Utilizar un diseño profesional, sobrio y de una sola columna.
- Mantener una estructura compatible con sistemas ATS.
- Guardar el documento generado y enviarlo al usuario mediante Telegram.

## 6. Historial de adaptaciones

- Registrar cada adaptación exitosa (que generó PDF).
- Guardar la fecha, el contenido de la oferta, el CV adaptado, el porcentaje de cumplimiento, la fuente de la oferta (proporcionada por el usuario: URL, portal, etc.) y la referencia al PDF.
- Permitir consultar las adaptaciones anteriores mediante el comando `/historial`.
- Permitir eliminar un registro del historial (y su PDF) mediante `/eliminar <id>`.

## 7. Funcionalidades futuras

Estas funcionalidades no forman parte del MVP:

- Gestión de múltiples usuarios.
- Descarga de documentos anteriores desde Telegram.
- Soporte para proveedores LLM adicionales.
- Generación de otros formatos, como DOCX.
- Despliegue mediante Webhook en un VPS.
- Integración con PostgreSQL.

---

## Alcance del MVP

La primera versión debe permitir completar el siguiente proceso:

**Enviar oferta → Analizar → Adaptar CV → Validar contenido → Generar PDF → Recibir documento.**

El MVP se considera funcional cuando el usuario puede completar este proceso desde Telegram sin intervención manual en los archivos internos del proyecto.
# AGENTS.md – Instrucciones para el agente de IA

## 1. Objetivo

Desarrollar el proyecto Perfilia siguiendo la documentación existente. Debes utilizar los documentos del repositorio /sdd como referencia principal antes de implementar cualquier funcionalidad.

El objetivo es construir un bot de Telegram que adapte currículums a ofertas laborales y genere documentos PDF compatibles con sistemas ATS.

## 2. Documentación del proyecto

Antes de comenzar cualquier tarea, lee los siguientes documentos en este orden:

1. `constitution.md`: contiene las reglas y principios obligatorios del proyecto.
2. `architecture.md`: explica las tecnologías, estructura y funcionamiento del sistema.
3. `features.md`: define las funcionalidades que debe implementar el proyecto.
4. `tasks.md`: contiene las tareas pendientes y el orden de desarrollo.

Todos los documentos deben interpretarse de manera conjunta.

## 3. Reglas de ejecución

- Respeta siempre las reglas de `constitution.md`.
- Utiliza `architecture.md` como referencia para la organización del código.
- Implementa únicamente funcionalidades definidas en `features.md` o aprobadas posteriormente.
- Utiliza `tasks.md` para controlar el avance del desarrollo.
- Trabaja en el orden establecido en las fases de `tasks.md`.
- No implementes todas las funcionalidades de una sola vez.
- Completa y verifica cada tarea antes de continuar con la siguiente.
- Marca una tarea como completada únicamente cuando esté implementada y probada.

## 4. Forma de trabajo

Para cada tarea:

1. Revisa su objetivo y los documentos relacionados.
2. Analiza el código existente antes de modificarlo.
3. Implementa la solución más sencilla que cumpla los requisitos.
4. Ejecuta las pruebas correspondientes.
5. Corrige los errores encontrados.
6. Actualiza `tasks.md` cuando la tarea esté terminada.
7. Informa brevemente qué se implementó y qué queda pendiente.

Si una tarea depende de otra, implementa primero la dependencia.

## 5. Restricciones

- No inventes requisitos ni agregues funcionalidades por iniciativa propia.
- No introduzcas tecnologías diferentes a las definidas en `architecture.md` sin justificación y aprobación.
- No compliques la arquitectura innecesariamente.
- No elimines funcionalidades existentes sin autorización.
- No modifiques el CV base durante una adaptación.
- Nunca permitas generar un PDF si la validación de fidelidad no fue satisfactoria.
- No marques tareas como completadas sin haberlas verificado.

## 6. Manejo de dudas y decisiones

Si encuentras información incompleta, contradictoria o una decisión técnica que pueda cambiar el funcionamiento del proyecto:

- Detén únicamente la tarea afectada.
- Explica brevemente el problema.
- Propón una solución concreta.
- Espera aprobación cuando la decisión implique cambiar los requisitos, tecnologías o reglas del proyecto.

Para decisiones menores de implementación, utiliza la alternativa más sencilla y coherente con la documentación.

## 7. Comunicación

Al finalizar cada tarea o grupo de tareas, informa:

- Qué se implementó.
- Qué archivos se crearon o modificaron.
- Qué pruebas se ejecutaron y sus resultados.
- Qué tareas quedan pendientes.
- Si existe algún problema que requiera intervención del usuario.

Evita explicaciones excesivamente técnicas o documentación innecesaria.

## 8. Instrucción inicial

Al iniciar el proyecto:

1. Lee toda la documentación indicada.
2. Inspecciona los archivos existentes del repositorio.
3. Identifica la primera tarea pendiente en `tasks.md`.
4. Comprueba si existen dependencias o configuraciones necesarias.
5. Comienza con la primera tarea de la Fase 1.

**Importante:** trabaja de forma incremental. No avances a la siguiente fase hasta verificar que la anterior funciona correctamente.

La prioridad es construir un MVP funcional, sencillo, mantenible y fiel a los requisitos documentados.
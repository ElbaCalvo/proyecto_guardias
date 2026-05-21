# Módulo de Presencia y Hardware

Este módulo implementa el control diario de fichajes, aislando el comportamiento de la capa física para permitir su ejecución bajo cualquier arquitectura de desarrollo.

## Arquitectura del Control de Asistencia

- **Modo Hardware Real:** Si la aplicación detecta la librería física `mfrc522`, el sistema activa el bucle de escucha del chip de radiofrecuencia. El flujo de ejecución web se pausa controladamente esperando que un docente aproxime su llavero o tarjeta UID.
- **Bypass en Modo Local:** Si el script se ejecuta en un PC común de desarrollo (donde el módulo de hardware no puede importarse), el sistema captura la excepción, conmuta de forma transparente a *Modo Local* y permite gestionar los fichajes haciendo clic manual en las tarjetas visuales de la interfaz web.
- **Consistencia Diaria:** El sistema invoca automáticamente limpiezas periódicas para asegurar que los estados de presencia de jornadas anteriores no afecten los cálculos automatizados del día actual.
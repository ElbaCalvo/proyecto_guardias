# Sistema de Gestión de Guardias y Control de Presencia

Este proyecto implementa una aplicación desarrollada en Python, diseñada para ser desplegada en un entorno educativo, que permite optimizar y automatizar los flujos de gestión interna del profesorado del instituto.

## Características Principales

- **Control de Presencia Híbrido:** Registro del estado de asistencia de los docentes a través de la interfaz web o mediante la integración de un lector de hardware físico RFID.
- **Detección Automática de Ausencias:** Sistema inteligente basado en franjas horarias que marca la inasistencia si un profesor tiene asignada una clase y no ha fichado a tiempo.
- **Motor de Guardias por Prioridades:** Cálculo y ordenación automatizada de los profesores sustitutos idóneos en base a las reglas de negocio del centro.
- **Gestión en Tiempo Real:** Interfaz web ligera y responsiva construida con Flask y maquetada con Bootstrap 5 para el registro y eliminación de guardias asignadas.
- **Persistencia Segura:** Gestión de datos estructurada mediante una base de datos SQLite con soporte para integridad referencial.
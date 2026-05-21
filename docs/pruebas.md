# Pruebas Unitarias

La aplicación se ha desarrollado siguiendo principios de diseño testeable, aislando por completo la lógica matemática del motor de las dependencias externas como bases de datos o hardware físico.

## Suite de Test Automatizados

En el archivo `test_motor.py` se implementa una batería de pruebas basadas en el framework nativo **unittest**:

- **Uso de Fixtures:** Se definen objetos simulados en memoria de la clase `ProfesorDisponible` con estadísticas complejas configuradas ad-hoc.
- **Aislamiento Total:** El test evalúa directamente la función pura `aplicar_prioridad()`, demostrando que los algoritmos de ordenación en cascada y desempate resuelven los conflictos de prioridad exactamente como exige la especificación técnica del PDF.
- **Ejecución Directa:** El script incluye un punto de entrada estándar para ser lanzado desde la consola web con el comando `python test_motor.py` garantizando reportes limpios e instantáneos de éxito o fallo.

## Checklist Final de Validación

A continuación se resume el estado de cumplimiento de los requisitos técnicos y funcionales del proyecto:

| ID | Requisito del Proyecto | Estado |
|:---|:---|:---:|
| 01 | Inicialización de base de datos (`ies.db`) | ✅ |
| 02 | Motor de guardias (Lógica de prioridades) | ✅ |
| 03 | Registro de presencia funcional | ✅ |
| 04 | Abstracción con `db_manager.py` | ✅ |
| 05 | Configuración de servicio `systemd` | ✅ |
| 06 | Navegación en Modo Kiosko | ✅ |
| 07 | Suite de tests unitarios | ✅ |
| 08 | Desactivación de `FLASK_DEBUG` en producción | ✅ |
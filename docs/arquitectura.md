# Arquitectura del Sistema

El sistema sigue una arquitectura modular y testeable, basada en la separación clara entre:

- Capa de presentación (Flask)
- Capa de negocio (guardias)
- Capa de hardware (presencia)
- Capa de datos (SQLite + db_manager)

```mermaid
graph TD
    Flask --> Motor
    Motor --> Reglas
    Motor --> DBManager
    Reglas --> ModelosDominio
    DBManager --> ModelosDatos
    Presencia --> DBManager
```
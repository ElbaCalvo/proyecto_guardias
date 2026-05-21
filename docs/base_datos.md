# Base de Datos (SQLite)

El sistema de persistencia de datos utiliza **SQLite**, garantizando una base de datos local ligera pero potente que no requiere un servidor independiente.

## Diseño de Persistencia e Integridad

- **Integridad Referencial:** Cada vez que el módulo `db_manager.py` establece una conexión, ejecuta de forma obligatoria la directiva `PRAGMA foreign_keys = ON` para asegurar que las restricciones entre tablas se cumplan estrictamente.
- **Inicialización Automatizada:** El script `init_db.py` es el encargado de leer el fichero estructural `schema.sql` para generar y construir las tablas limpias de forma automática.
- **Transaccionalidad Sólida:** Las operaciones críticas (como registrar una guardia e incrementar simultáneamente el contador del sustituto) se encapsulan bajo un contexto seguro (`with conn:`) asegurando un comportamiento atómico (*commit* o *rollback*).
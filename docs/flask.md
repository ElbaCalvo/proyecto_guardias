# Módulo Flask

El corazón del servidor web se ha desarrollado utilizando el microframework **Flask**, proporcionando un sistema de enrutamiento rápido, semántico y eficiente.

## Rutas y Controladores Principales

- `/` (`GET`): Renderiza la vista principal o panel de bienvenida tipo Kiosko del sistema.
- `/guardias` (`GET`): Panel de administración horaria que evalúa el reloj del sistema para lanzar la detección automática de ausencias y mostrar el ranking de sustitutos.
- `/registrar` (`POST`): Endpoint seguro que recibe los datos de un formulario para validar e insertar una nueva guardia.
- `/eliminar` (`POST`): Permite revocar o borrar un registro de guardia activa liberando el tramo horario.
- `/presencia` (`GET`): Muestra la lista interactiva de profesores del claustro junto con su estado actual de asistencia del día.
- `/toggle_presencia` (`POST`): Controlador híbrido que gestiona los cambios de estado combinando la entrada manual de la web con el lector de hardware físico.
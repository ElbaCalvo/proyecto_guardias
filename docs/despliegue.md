# Despliegue del Sistema

El software está optimizado para funcionar de forma continua, autónoma e ininterrumpida, ideal para ser desplegado en sistemas empotrados o mini-PCs instalados en las consolas de entrada del centro escolar.

## Directrices de Producción

1. **Instalación de Dependencias:** El entorno de producción requiere instalar las dependencias base de Flask junto con las extensiones del lector de tarjetas físicos (`mfrc522`) mediante el gestor de paquetes de Python.
2. **Configuración como Servicio del Sistema:** Para asegurar que la web se inicie automáticamente tras un corte de luz o un reinicio del hardware, se recomienda registrar el script `app.py` dentro de un archivo de configuración de servicio en el gestor `systemd` del sistema operativo (p. ej. `/etc/systemd/system/guardias.service`).
3. **Generación Exhaustiva de Documentación:** Ejecutando el comando `mkdocs build` en la raíz del entorno, el generador compila la estructura web estática y la empaqueta dentro de la carpeta `site/`, lista para ser servida por servidores web de alto rendimiento como Nginx o Apache.
from mfrc522 import SimpleMFRC522
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def leer_tarjeta():
    """
    Lee el UID de una tarjeta RFID utilizando el hardware MFRC522.
    Devuelve el UID como un string.
    """
    lector = SimpleMFRC522()
    try:
        id_tarjeta, texto = lector.read()
        return str(id_tarjeta)
    except Exception as e:
        print(f"Error accediendo a hardware: {e}")
        return None

def escribir_tarjeta(data_string):
    """
    Graba información en un tag RFID. 
    Uso estándar para inicialización de credenciales.
    """
    lector = SimpleMFRC522()
    
    try:
        logger.info(f"Escribiendo datos en tarjeta: {data_string}")
        lector.write(data_string)
        logger.info("Escritura completada correctamente.")
        return True
    except Exception as e:
        logger.error(f"Error al escribir en el tag RFID: {str(e)}")
        return False
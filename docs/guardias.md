# Motor de Cálculo de Guardias

La asignación de guardias se rige bajo un motor algorítmico automatizado encargado de evitar el favoritismo o la sobrecarga de trabajo del profesorado sustituto.

## Algoritmo de Prioridades en Cascada

Cuando ocurre una ausencia, el sistema recopila los datos de los profesores disponibles (aquellos que están en el centro y tienen esa hora marcada como libre en su horario) y les aplica tres criterios estrictos de ordenación en cascada mediante una tupla lambda de Python:

1. **1ª Prioridad (Global):** Se sitúa al principio del ranking al profesor que posea el **MENOR número de guardias totales acumuladas** a lo largo del curso.
2. **2ª Prioridad (Semanal):** En caso de empate en el acumulado global, el motor prioriza a aquel profesor que **MENOS guardias haya realizado durante la semana actual**.
3. **3ª Prioridad (Carga lectiva):** Si persiste el empate, el sistema selecciona al docente con la **MENOR carga lectiva** horaria asignada en su contrato.
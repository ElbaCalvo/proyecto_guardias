import unittest
from modules.guardias.models import ProfesorDisponible
from modules.guardias.reglas import aplicar_prioridad

class TestMotorGuardias(unittest.TestCase):

    def test_criterio_prioridades_ranking(self):
        """Verifica que el motor ordena correctamente según los criterios del PDF"""
        
        profesor_A = ProfesorDisponible(1, "Carlos García", total_guardias=5, guardias_semana=2, carga_lectiva=18)
        profesor_B = ProfesorDisponible(2, "Ana López", total_guardias=2, guardias_semana=1, carga_lectiva=20)
        profesor_C = ProfesorDisponible(3, "Luis Martínez", total_guardias=2, guardias_semana=0, carga_lectiva=19)
        
        lista_candidatos = [profesor_A, profesor_B, profesor_C]
        
        ranking_calculado = aplicar_prioridad(lista_candidatos)
        

        self.assertEqual(ranking_calculado[0].nombre, "Luis Martínez")
        self.assertEqual(ranking_calculado[1].nombre, "Ana López")
        self.assertEqual(ranking_calculado[2].nombre, "Carlos García")

if __name__ == "__main__":
    unittest.main()
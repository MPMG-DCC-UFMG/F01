import unittest
from src.validadores.licitacoes import ValidadorLicitacoes
import pandas as pd

# To execute this test file:
# F01/src$ python -m unittest tests.test_licitacoes

class TestLicitacoes(unittest.TestCase):

    def test_explain(self):

        validador = ValidadorLicitacoes({}, None, None)
        col_name = 'n'
        df = pd.DataFrame({col_name:[1,2,3]})
        
        result = validador.explain(df, col_name)

        expected = 'Explain - Quantidade de entradas analizadas: 3'\
                    +'\n\tQuantidade de entradas válidas: 6\n'

        self.assertEqual(expected, result, "Resposta não é a esperada.")


if __name__ == '__main__':
    unittest.main()
import os
import unittest
from pathlib import Path
from src.validadores.utils.path_functions import list_files
from src.validadores.utils.compressao import extrair_arquivos

# To execute this test file:
# F01/src$ python -m unittest tests.test_utils.test_compressao

BASE_PATH = Path(os.getcwd()) / 'tests/test_utils/test_compressao_arquivos'
BASE_PATH = Path(BASE_PATH)

TEST_EXTRAIR_FOLDER = BASE_PATH / "test_extrair"
RESULT_EXTRAIR_FOLDER = BASE_PATH / "result_extrair"

class TestCompressao(unittest.TestCase):

    def test_extrair_arquivos_rar_com_extensao(self):

        # Rar com extensão

        extrair_arquivos(TEST_EXTRAIR_FOLDER / "rar" / "com_extensao", RESULT_EXTRAIR_FOLDER / "rar" / "com_extensao")
        files = list_files(RESULT_EXTRAIR_FOLDER / "rar" / "com_extensao")

        result = [x.replace(os.getcwd() + '/tests/test_utils/test_compressao_arquivos/result_extrair/rar/com_extensao/', '') for x in files]

        expected = ['instrumentos-planejamento/LDO/ANEXOS LDO  2021.xlsx', 'instrumentos-planejamento/LDO/LDO-2147-30072018.pdf', 'instrumentos-planejamento/LDO/LDO-2160-11122018.pdf', 'instrumentos-planejamento/LDO/Lei nº 2229.2020 - Altera Lei nº 2213.2020 (LDO 2021- substitui anexo e inclui dispositivos na redação).pdf', 'instrumentos-planejamento/LDO/lei-1852-LDO-2010.pdf', 'instrumentos-planejamento/LDO/lei-1876-LDO-2011.pdf', 'instrumentos-planejamento/LDO/lei-1907-LDO-2012.pdf', 'instrumentos-planejamento/LDO/lei-1937-LDO-2013.pdf', 'instrumentos-planejamento/LDO/lei-1988-LDO-2014.pdf', 'instrumentos-planejamento/LDO/lei-2051-LDO-2015.pdf', 'instrumentos-planejamento/LDO/lei-2090-LDO-2016.pdf', 'instrumentos-planejamento/LDO/lei-2120-LDO-2017.pdf', 'instrumentos-planejamento/LDO/lei-2130-LDO-2017.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/metas-anuais.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/metas-fiscais-01.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/metas-fiscais-02.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/metas-fiscais-03.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/metas-prioridades.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/patrimonio-liquido.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/riscos-fiscais.pdf', 'instrumentos-planejamento/LOA/ANEXO_LOA.PDF1.rar', 'instrumentos-planejamento/LOA/Lei nº 2228.2020 - Lei Orçamentária Anual para o exercício de 2021.pdf', 'instrumentos-planejamento/LOA/lei-1831-LOA-2009.pdf', 'instrumentos-planejamento/LOA/lei-1858-LOA-2010.pdf', 'instrumentos-planejamento/LOA/lei-1889-LOA-2011.pdf', 'instrumentos-planejamento/LOA/lei-1919-LOA-2012.pdf', 'instrumentos-planejamento/LOA/lei-1958-LOA-2013.pdf', 'instrumentos-planejamento/LOA/lei-2027-LOA-2014.pdf', 'instrumentos-planejamento/LOA/lei-2039-LOA-2015.pdf', 'instrumentos-planejamento/LOA/lei-2074-LOA-2015.pdf', 'instrumentos-planejamento/LOA/lei-2108-LOA-2016.pdf', 'instrumentos-planejamento/LOA/lei-2109-LOA-2016.pdf', 'instrumentos-planejamento/LOA/lei-2128-LOA-2017.pdf', 'instrumentos-planejamento/LOA/LOA-2159-11122018.pdf', 'instrumentos-planejamento/LOA/LOA-2163-27122018.pdf', 'instrumentos-planejamento/PPA/Lei nº 2230.2020 - Altera Lei nº 2127.2017 (PPA 2018-2021 - substitui anexo e inclui dispositivo na redação).pdf', 'instrumentos-planejamento/PPA/Lei-1.952-14.pdf', 'instrumentos-planejamento/PPA/lei-1829.09-ppa-2010-2013.pdf', 'instrumentos-planejamento/PPA/lei-2127-PPA-2017.pdf', 'instrumentos-planejamento/PPA/PPA-2018.rar', 'instrumentos-planejamento/PPA/PPA-2161-11122018.pdf']

        self.assertEqual(expected, result, "Resposta não é a esperada.")

        for path_file in files:
            try:
                os.remove(path_file)
            except OSError as e:
                print(f"Error:{ e.strerror}")


    def test_extrair_arquivos_rar_sem_extensao(self):

        # Rar sem extensão

        extrair_arquivos(TEST_EXTRAIR_FOLDER / "rar" / "sem_extensao", RESULT_EXTRAIR_FOLDER / "rar" / "sem_extensao")
        files = list_files(RESULT_EXTRAIR_FOLDER / "rar" / "sem_extensao")

        result = [x.replace(os.getcwd() + '/tests/test_utils/test_compressao_arquivos/result_extrair/rar/sem_extensao/', '') for x in files]

        expected = ['instrumentos-planejamento/LDO/ANEXOS LDO  2021.xlsx', 'instrumentos-planejamento/LDO/LDO-2147-30072018.pdf', 'instrumentos-planejamento/LDO/LDO-2160-11122018.pdf', 'instrumentos-planejamento/LDO/Lei nº 2229.2020 - Altera Lei nº 2213.2020 (LDO 2021- substitui anexo e inclui dispositivos na redação).pdf', 'instrumentos-planejamento/LDO/lei-1852-LDO-2010.pdf', 'instrumentos-planejamento/LDO/lei-1876-LDO-2011.pdf', 'instrumentos-planejamento/LDO/lei-1907-LDO-2012.pdf', 'instrumentos-planejamento/LDO/lei-1937-LDO-2013.pdf', 'instrumentos-planejamento/LDO/lei-1988-LDO-2014.pdf', 'instrumentos-planejamento/LDO/lei-2051-LDO-2015.pdf', 'instrumentos-planejamento/LDO/lei-2090-LDO-2016.pdf', 'instrumentos-planejamento/LDO/lei-2120-LDO-2017.pdf', 'instrumentos-planejamento/LDO/lei-2130-LDO-2017.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/metas-anuais.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/metas-fiscais-01.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/metas-fiscais-02.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/metas-fiscais-03.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/metas-prioridades.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/patrimonio-liquido.pdf', 'instrumentos-planejamento/LDO/anexos-LDO-2017/riscos-fiscais.pdf', 'instrumentos-planejamento/LOA/ANEXO_LOA.PDF1.rar', 'instrumentos-planejamento/LOA/Lei nº 2228.2020 - Lei Orçamentária Anual para o exercício de 2021.pdf', 'instrumentos-planejamento/LOA/lei-1831-LOA-2009.pdf', 'instrumentos-planejamento/LOA/lei-1858-LOA-2010.pdf', 'instrumentos-planejamento/LOA/lei-1889-LOA-2011.pdf', 'instrumentos-planejamento/LOA/lei-1919-LOA-2012.pdf', 'instrumentos-planejamento/LOA/lei-1958-LOA-2013.pdf', 'instrumentos-planejamento/LOA/lei-2027-LOA-2014.pdf', 'instrumentos-planejamento/LOA/lei-2039-LOA-2015.pdf', 'instrumentos-planejamento/LOA/lei-2074-LOA-2015.pdf', 'instrumentos-planejamento/LOA/lei-2108-LOA-2016.pdf', 'instrumentos-planejamento/LOA/lei-2109-LOA-2016.pdf', 'instrumentos-planejamento/LOA/lei-2128-LOA-2017.pdf', 'instrumentos-planejamento/LOA/LOA-2159-11122018.pdf', 'instrumentos-planejamento/LOA/LOA-2163-27122018.pdf', 'instrumentos-planejamento/PPA/Lei nº 2230.2020 - Altera Lei nº 2127.2017 (PPA 2018-2021 - substitui anexo e inclui dispositivo na redação).pdf', 'instrumentos-planejamento/PPA/Lei-1.952-14.pdf', 'instrumentos-planejamento/PPA/lei-1829.09-ppa-2010-2013.pdf', 'instrumentos-planejamento/PPA/lei-2127-PPA-2017.pdf', 'instrumentos-planejamento/PPA/PPA-2018.rar', 'instrumentos-planejamento/PPA/PPA-2161-11122018.pdf']

        self.assertEqual(expected, result, "Resposta não é a esperada.")

        for path_file in files:
            try:
                os.remove(path_file)
            except OSError as e:
                print(f"Error:{ e.strerror}")

    def test_extrair_arquivos_zip_com_extensao(self):

        # Zip com extensão
        print(RESULT_EXTRAIR_FOLDER)

        extrair_arquivos(TEST_EXTRAIR_FOLDER / "zip" / "com_extensao", RESULT_EXTRAIR_FOLDER / "zip" / "com_extensao")
        files = list_files(RESULT_EXTRAIR_FOLDER / "zip" / "com_extensao")

        result = [x.replace(os.getcwd() + '/tests/test_utils/test_compressao_arquivos/result_extrair/zip/com_extensao' + os.getcwd(), '') for x in files]
        expected = ['/tests/test_utils/test_compactar_arquivos/test_compactar/pdf_file_test.pdf', '/tests/test_utils/test_compactar_arquivos/test_compactar/xlsx_files_test.xlsx', '/tests/test_utils/test_compactar_arquivos/test_compactar/test_licitacoes.py']
        self.assertEqual(expected, result, "Resposta não é a esperada.")

        for path_file in files:
            try:
                os.remove(path_file)
            except OSError as e:
                print(f"Error:{ e.strerror}")
    

    def test_extrair_arquivos_zip_sem_extensao(self):

        # Zip sem extensão

        extrair_arquivos(TEST_EXTRAIR_FOLDER / "zip" / "sem_extensao", RESULT_EXTRAIR_FOLDER / "zip" / "sem_extensao")
        files = list_files(RESULT_EXTRAIR_FOLDER / "zip" / "sem_extensao")

        result = [x.replace(os.getcwd() + '/tests/test_utils/test_compressao_arquivos/result_extrair/zip/sem_extensao' + os.getcwd(), '') for x in files]
        expected = ['/tests/test_utils/test_compactar_arquivos/test_compactar/pdf_file_test.pdf', '/tests/test_utils/test_compactar_arquivos/test_compactar/xlsx_files_test.xlsx', '/tests/test_utils/test_compactar_arquivos/test_compactar/test_licitacoes.py']
        self.assertEqual(expected, result, "Resposta não é a esperada.")

        for path_file in files:
            try:
                os.remove(path_file)
            except OSError as e:
                print(f"Error:{ e.strerror}")


if __name__ == '__main__':
    unittest.main()



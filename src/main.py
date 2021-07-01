import sys
sys.path.insert(1, './classifiers')


from faq import predict_faq, explain_faq
from concursos import predict_copia_edital, explain_copia_edital, predict_recursos, explain_recursos

if __name__ == "__main__":
    faq_dict = predict_faq()
    explain_faq(faq_dict)

    concursos_dict = predict_copia_edital()
    explain_copia_edital(concursos_dict)
    
    concursos_dict = predict_recursos()
    explain_recursos(concursos_dict)




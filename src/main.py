import sys
sys.path.insert(1, './classifiers')

from faq import predict_faq, explain_faq
from diaria_viagem import predict_diaria_viagem, explain_diaria_viagem

if __name__ == "__main__":

    faq_dict = predict_faq()
    explain_faq(faq_dict)


    df = predict_diaria_viagem()
    explain_diaria_viagem(df)




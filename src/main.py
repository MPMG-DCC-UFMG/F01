import sys
sys.path.insert(1, './classifiers')

from faq import predict_faq, explain_faq

if __name__ == "__main__":
    faq_dict = predict_faq()
    explain_faq(faq_dict)




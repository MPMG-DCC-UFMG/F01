import os
from pdf2image import convert_from_path

path = '/home/asafe/GitHub/Coleta_C01/Para_de_Minas/esic/data/files/'
name_file = '62507a47ea4e1f89b6a78b3c03a5b880.pdf.pdf'

dir = path + name_file.split(".")[0]
os.makedirs(dir)

pdfs = ('{}/{}'.format(path, name_file))
pages = convert_from_path(pdfs, 350)

i = 1
for page in pages:
    image_name = dir + "/Page_" + str(i) + ".jpg"  
    page.save(image_name, "JPEG")
    i += 1     


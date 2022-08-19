print('Hello Friend')

import os
import pandas as pd
from script.functions import decrypt_load, get_pages, get_pdf_tables, get_pdf_text
from script.variables import paths

#################################### PREPARATION ####################################
# Selecting correct path out of ones specified in variables file
for i in paths:
    if os.path.isdir(i) == True:
        pth = i
    else:
        continue 
pdf_dir = os.listdir(pth)


# Listing out file names
pdf_list = []
for file in pdf_dir:
    pdf_list.append(file)

# Decrypting pdfs and overwriting them
decrypt_load(pdf_list, pth)


#################################### EXTRACTION ####################################
# getting path to desktop on device for writing the files
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# Identyfying pages which contain keywords
pdf_pages = get_pages(pdf_list, pth)

# Extraction of tables from previously listed out pages
extracted_tables = get_pdf_tables(pdf_pages, pth)
extracted_tables.to_csv(desktop+'/pdftables.csv', sep=';', encoding='UTF-8')

# Extraction of text from previously listed pages
extracted_text = get_pdf_text(pdf_pages, pth)
extracted_text.to_csv(desktop+'/pdftext.csv', sep=';', encoding='UTF-8')

print('Goodbye Friend')
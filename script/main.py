print('Hello Friend')

import sys, os
import re
import pandas as pd
from script.functions import decrypt_load, get_pages, get_pdf_tables, get_pdf_text
from script.variables import paths, key_words, keywords_pay, write_path

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

# Identyfying pages which contain keywords
pdf_pages = get_pages(pdf_list)

# Extraction of tables from previously listed out pages
extracted_tables = get_pdf_tables(pdf_pages)
extracted_tables.to_csv(write_path, sep=',', encoding='latin1')

# Extraction of text from previously listed pages
extracted_text = get_pdf_text(pdf_pages)
#extracted_text.to_csv(write_path, sep=',', encoding='latin1')

print('Goodbye Friend')
print('Hello Friend')

import sys, os
import re
import pandas as pd
from script.functions import get_pdf_tables, get_pdf_text
from script.variables import pth, key_words, keywords_pay

#pdf_dir = os.listdir(pth)
pdf_list = []
#for file in pdf_dir:
#    pdf_list.append(file)


extracted_text = get_pdf_text(pdf_list)


extracted_tables = get_pdf_tables()
extracted_tables.to_csv(r"", sep=',', encoding='latin1')
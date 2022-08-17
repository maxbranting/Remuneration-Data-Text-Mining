print('Hello Friend')

import sys, os
import PyPDF2
import re
import pandas as pd
import pikepdf
import camelot
from .functions import pdf_tables_to_df
from script.variables import pth, key_words, keywords_pay
from functions import get_pages, pdf_tables_to_df

#pdf_dir = os.listdir(pth)
pdf_list = []
#for file in pdf_dir:
#    pdf_list.append(file)


get_pages(pdf_list)



pdf_tables_to_df()
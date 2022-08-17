print('Hello Friend')

import sys, os
import PyPDF2
import re
import pandas as pd
import pikepdf
import camelot
from script.variables import pth, key_words, keywords_pay
from functions import get_pages

pdf_dir = os.listdir(pth)
pdf_list = []
for file in pdf_dir:
    pdf_list.append(file)


get_pages(pdf_list)



for title, pages in pdf_pages.items():
    #list for documents that had no tables
    notabpdfs = []
    #empty list of dataframes
    tempdfs = []
    for page in pages:
        #converting page to str for camelot read
        cpage = str(page)
        #reading in the tables in given pages
        tables = camelot.read_pdf(pth + '/' + title, pages=cpage)
        if len(tables)==0:
            notabpdfs.append(title)
        else:    
            for i in range(len(tables)):
                tempdf = tables[i].df
                #deleting last 4 chars in title which is the ".pdf" part
                tempdf['Institution_year'] = title[:-4]
                # appending temporary dfs to a list
                tempdfs.append(tempdf)
                #concatanating all temporary dfs from the page
                dfconc = pd.concat(tempdfs)
                # concatanating newest version of  dftext by tables from the page
                dftext = pd.concat([dftext, dfconc], axis = 0, ignore_index = True)
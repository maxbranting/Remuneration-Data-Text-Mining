import sys, os
import PyPDF2
import re
import pandas as pd
import pikepdf
import camelot
from script.variables import pth, key_words, keywords_pay

word_set_1 = set(key_words['exec'])
word_set_2 = set(key_words['pay'])

def get_pages(pdf_list):
    """
    Returns a dictionary containing pdf file name and numbers of pages where keywords have been found.

    """
    pdf_pages = []
    for element in pdf_list:
        document = PyPDF2.PdfFileReader(pth + '/' + element, strict=False)
        # here we retrieve number of pages to enable us to iterate through them below
        no_pages = document.getNumPages()
        # defining list for page numbers
        pagenum_list=[]
        for i in range(no_pages):
            # extracting text from a page and florring the letters
            text = document.getPage(i).extractText().lower()
            # set and split allows us to later iterate throug words
            text_set = set(text.split())
            if word_set_1.intersection(text_set) and word_set_2.intersection(text_set):
                # appending list with page numbers
                pagenum_list.append(i)
        # appending dictionary of lists
        pdf_pages[element] = pagenum_list
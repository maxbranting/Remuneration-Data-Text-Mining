import pandas as pd
import pikepdf
import PyPDF2
import camelot
from script.variables import key_words, keywords_pay


def decrypt_load(pdf_list:list, pth):
    """
    Decrypts pdf files in given directory and overwrites them.

    Arguments
    ------
    pdf_list: list of pdf file names.
    pth: path in which pdf's are stored.
    """
    for n in pdf_list:
        pdf = pikepdf.open(pth + '/' + n, allow_overwriting_input=True)
        pdf.save(pth + '/' + n) 


def get_pages(pdf_list:list, pth) -> dict:
    """
    Returns a dictionary containing pdf file name and numbers of pages where keywords have been found.
    
    Arguments
    -------
    pdf_list: list of pdf file names.
    pth: path where pdf files are stored.

    """
    word_set_1 = set(key_words['exec'])
    word_set_2 = set(key_words['pay'])
    pdf_pages = {}
    evaded_pdfs = []
    for element in pdf_list:
        try:
            print(f'Reading in document {element}')
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
            print(f'Found {len(pagenum_list)} pages containging keywords in {element}')
        except UnicodeDecodeError:
            #evaded_pdfs.append(element)
            #print(f'Could not get pages for {element}')
            pass

    print(f'Found keywords in documents {pdf_pages.keys()} /n Could not scan through {evaded_pdfs}')



def get_pdf_tables(pdf_pages:dict, pth) -> pd.DataFrame:
    """
    Downloads tables from pdf to a dataframe.
    
    Arguments
    -------
    pdf_pages: dictionary where keys are names of files and values are numbers of pages.
    pth: path where pdf files are stored.

    How to use
    -------
    Assign the function to a variable. The function will return concatanated tables as a dataframe
    """


    for title, pages in pdf_pages.items():
        print(f'Searching for tables in {title}')
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
    return dftext


def get_pdf_text(pdf_pages:dict, pth) -> pd.DataFrame:
    """
    Searches for keywords on pages that cointain them. If found extracts 50 words before and 50 words after the keyword.
    
    Arguments
    -------
    pdf_pages: dictionary where keys are names of files and values are numbers of pages.
    pth: path where pdf files are stored.

    How to use
    -----
    Assign to a variable, the function will return a dictionary of filename and its page as key and a list of words as value.
    """

    remuntext_dict = {}
    for title, pages in pdf_pages.items():
        print(f'Searching for text in {title}')
        document = PyPDF2.PdfFileReader(pth + '/' + title, strict=False)
        for page in pages:
            textsplit = document.getPage(page).extractText().lower().split()
            for index, item in enumerate(textsplit):
                if item in keywords_pay:
                    dictitle = (str(title) + ' page ' + str(page))
                    remuntext_dict[dictitle] = textsplit[index-50:index+50]
                    print('Keywords found /n Extracting text')
    remuntext_dict = {index: ' '.join(values) for index, values in remuntext_dict.items()}
    remuntext_df = pd.DataFrame.from_dict(remuntext_dict, orient = 'index')
    return remuntext_df
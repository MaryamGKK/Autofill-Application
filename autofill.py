from bs4 import BeautifulSoup
from nltk import trigrams, bigrams
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
import requests
import msvcrt
import pickle
import bs4
import re
import PyPDF2
import sys
from tkinter import *
import tkinter as tk

# next two functions are used for collecting corpus
def webScrape():
    corpus = ''
    urlsList = ['https://en.wikipedia.org/wiki/History_of_Egypt', 'https://en.wikipedia.org/wiki/History_of_Japan#Prehistoric_and_ancient_Japan',
                'https://en.wikipedia.org/wiki/Ancient_Rome', 'https://en.wikipedia.org/wiki/Tamils', 'https://en.wikipedia.org/wiki/Ancient_Egypt',
                'https://www.britannica.com/place/ancient-Egypt/The-king-and-ideology-administration-art-and-writing']
    for url in urlsList:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        wiki = 'en.wikipedia' in url
        if not wiki :
            articleDiv = soup.find('section', {'id': 'ref'})
        else:
            articleDiv = soup.find('div', class_='mw-parser-output')
        for match in articleDiv:
            if not wiki:
                if str(match.name) == 'None':
                    continue
                for paragraph in match.find_all('p'):
                    try:
                        corpus += paragraph.get_text.strip()
                    except Exception as e:
                        pass
            else:
                if type(match) is not bs4.element.NavigableString and (match.name == 'p' or match.name == 'h2' or match.name == 'h3' or match.name == 'h4' or match.name == 'ul' ) :
                    try:
                        corpus += match.get_text().strip()
                    except Exception as e:
                        pass

        print('done with ', url)
    #with open('fname.txt', "w+", encoding="utf-8") as f:
    #    f.write(corpus)
    return corpus


def bookParsing():
    # books = ['fea.pdf', 'g.pdf', 'n.pdf', 'p.pdf']
    books = ['a.pdf',  'd.pdf']
    string = ''
    for book in books:
        pdf_file = open(book, 'rb')
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        for i in range(number_of_pages - 1):
            page = read_pdf.getPage(i)
            page_content = page.extractText()
            string += page_content
        #print(page_content.strip())
        print("book : ", book, " finished")
    #with open('book.txt', 'w+', encoding='utf-8') as f:
    #    f.write(string)
    return string


def sentenceTokenize(text):
    # number_of_words = 0
    model = defaultdict(lambda: defaultdict(lambda: 0))  # this is a 2-d dictionary for getting hits with every word
    sentences = sent_tokenize(text)
    characters_to_remove = "!,().?@:"  # using regular exp to filter sentence
    pattern = "[" + characters_to_remove + "]"
    for sentence in sentences:
        sentence = re.sub(pattern, " ", sentence)
        sentence = sentence.split()
        # number_of_words += len(sentence)
        countOfWords = 0
        while countOfWords < len(sentence) - 2:
            word1 = sentence[countOfWords]
            word2 = sentence[countOfWords + 1]
            word3 = sentence[countOfWords + 2]
            model[(word1, word2)][word3] += 1
            countOfWords += 1

    for w1_w2 in model:
        totalCount = float(sum(model[w1_w2].values()))
        for w3 in model[w1_w2]:
            model[w1_w2][w3] /= totalCount
    # print(number_of_words)
    return model


# this function is for searching inside corpus, model is the corpus and word1 word2 are the search words
def searchOnData(model, word1, word2):
    topHitsDictionary = {k: v for k, v in sorted(dict(model[word1, word2]).items(), key=lambda item: item[1], reverse=True)} # this dictionary contains results with higest probability
   # print(topHitsDictionary)
    return topHitsDictionary


# the next two functions are for loading and saving corpus
def saveData(objectToBeSaved):
    corp = open('corpus', 'ab')
    pickle.dump(objectToBeSaved, corp)
    corp.close()


def loadData():
    print("loading data")
    corp = open('corpus', 'rb')
    loadedCorpus = pickle.load(corp)
    corp.close()
    print('finished loading')
    return loadedCorpus

def printInput():
    data = loadData()
    trigramData = sentenceTokenize(data)
    query = ''
    word1 = inputtxt.get(1.0, "end-1c")
    if len(word1.split()) > 1:
        splitedQuery = word1.split()
        mydict = searchOnData(trigramData, splitedQuery[-2], splitedQuery[-1])
        first5 = {k: mydict[k] for k in list(mydict)[:5]}
    print(first5)
    i = 1
    my_list.delete(0,'end')
    for k in first5:
        my_list.insert(i,word1+' '+k)
        i+=1
# to show options to complete with enter button should be pressed
# the corpus is mainly about history ancient egypt and greece..etc

if __name__ == '__main__':
    # Top level window
    frame = tk.Tk()
    frame.title("Search")
    frame.geometry('500x300')
    # Function for getting Input
    # from textbox and printing it
    # at label widget
    
    
    # TextBox Creation
    inputtxt = tk.Text(frame,
    				height = 1,
    				width = 20)
    
    inputtxt.pack()
    
    # Button Creation
    printButton = tk.Button(frame,
    						text = "Search",
    						command = printInput)
    printButton.pack()
    
    # Label Creation
    my_list = tk.Listbox(frame, width=50)
    my_list.pack(pady=40)
    
    frame.mainloop()

   
       
    
    




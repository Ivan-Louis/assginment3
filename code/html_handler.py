from __future__ import division
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.vocabulary = []
        self.current_tag = 0
        self.docs = []
        self.doc_id = 0
        self.dict = {}
        self.ini = 0
    def get_vocabulary(self):
        return " ". join(self.vocabulary)

    def get_docs(self):
        return self.docs

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if self.current_tag == "docno":
            self.ini = 1
        #print(tag)

    def handle_endtag(self, tag):
        self.current_tag = tag
        if self.current_tag == "docno":
            self.ini = 0
        if self.current_tag == "doc":
            if self.doc_id != 0:
                print(self.doc_id)
                self.dict['id'] = self.doc_id
                self.dict['content'] = self.get_vocabulary()
                self.docs.append(self.dict)
                self.vocabulary = []
                self.dict = {}

    def handle_data(self, data):
        #print(self.current_tag)
        if self.current_tag == "docno" and self.ini == 1:
            #TODO legg til ny index i dic

            self.doc_id = data
            #print(self.doc_id)
        #print(tag)


        if self.current_tag != "script" and self.current_tag != "style" and self.current_tag != "dochdr" and self.current_tag != "docno":
            data_words = data.split()
            for i in range(len(data_words)):
                self.vocabulary.append(data_words[i])



def handle_html(path):
    try:
        file = open(path, encoding="UTF-8")
    except:
        file = open(path, encoding="Latin-1")
    html = file.read()
    #print(html)
    parser = MyHTMLParser()
    parser.feed(html)
    vocabulary = parser.get_docs()
    return vocabulary


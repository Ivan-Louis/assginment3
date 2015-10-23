from __future__ import division
from html.parser import HTMLParser
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
import nltk
import re
stemmer = SnowballStemmer("english")

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.vocabulary = []
        self.current_tag = 0

    def get_vocabulary(self):
        return " ". join(self.vocabulary)

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_data(self, data):
        if self.current_tag == "docno":
            #TODO legg til ny index i dic
            if self.current_tag != "script" and self.current_tag != "style" and self.current_tag != "dochdr" and self.current_tag != "docno":
                data_words = data.split()
                for i in range(len(data_words)):
                    self.vocabulary.append(data_words[i])


def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def pre_process(input):
    tfidf_vector = TfidfVectorizer(max_df=0.8, min_df=0.01, max_features=2000,
                                 stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem)
    matrix = tfidf_vector.fit_transform(input)
    return matrix

def handle_html(path):
    file = open(path, encoding="UTF-8")
    html = file.read()
    #print(html)
    parser = MyHTMLParser()
    parser.feed(html)
    vocabulary = parser.get_vocabulary()
    return vocabulary






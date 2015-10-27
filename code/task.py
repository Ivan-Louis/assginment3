__author__ = 'Louis'

import os
from html_handler import handle_html
from vsmRetrieve import retrieveVsm
from whoosh.fields import Schema, TEXT, ID
import whoosh.index as index
from xml.dom import minidom
from bs4 import BeautifulSoup

#files and directories
indexDir = "../data/index"
inputDir = "../csiro-corpus"
outputFile = "../output/baseline.out"
queriesFile = "../data/queries.xml"
temp = "testdocs"

#for tag in soup.find_all(True):
#    print(tag)
"""
handle = handle_html(temp)
print(handle[0])
print(handle[1])
print(handle[2])
print(handle[3])
print(handle[4])

#print(handle)
"""
# Method for loading an xml file of queries

def loadQueries():
    queries = []
    xmldoc = minidom.parse(queriesFile)
    for query in xmldoc.getElementsByTagName("query"):
        id = query.getAttribute('id')
        text = query.firstChild.nodeValue
        queries.append({'id': id, 'text': text})

    return queries

# Creating the index. This calls the handle_html method that returns a dictionary with ID and content
# of each file under csiro-corpus
def createIndex():
    schema = Schema(id=ID(stored=True), content=TEXT)

    if not os.path.exists(indexDir):
        os.mkdir(indexDir)
    ix = index.create_in(indexDir, schema)

    writer = ix.writer()

    for file in os.listdir(inputDir):
        #print(file)
        fileloc = inputDir +"/"+ file
        docs = handle_html(fileloc)
        for doc in docs:
            try:
                writer.add_document(id=doc['id'].decode(),  content=doc['content'].decode())
            except:
                writer.add_document(id=doc['id'],  content=doc['content'])

    writer.commit()
    ix.close()

# Method for making the baseline retrival of the files. Uses vector space model with TFIDF
def makeBaseline(ixDir, outFile):
    ix = index.open_dir(ixDir)

    # Use the reader to get statistics
    reader = ix.reader()

    queries = loadQueries()

    outfile = open(outFile, "w")

    for query in queries:
        print("Processing query number", query['id'])

        # Retrieve documents using the vector space model
        res = retrieveVsm(reader, query['text'])

        # Output max 10 results
        for docnum in sorted(res, key=res.get, reverse=True)[:50]:
            # Look up our docID
            stored = reader.stored_fields(docnum)
            # Write `docID Q0 queryID score` into `data/cacm.out`
            outfile.write(query['id']+ " Q0 " + stored['id'] + " " + str(res[docnum]) + "\n")

    outfile.close()
    ix.close()

if __name__ == '__main__':
    #createIndex()  # note that this has to be done only once

    makeBaseline(indexDir, outputFile)
    print("done")

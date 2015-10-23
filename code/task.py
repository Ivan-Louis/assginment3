__author__ = 'Louis'

<<<<<<< HEAD
import os
from html_handler import handle_html
from vsmRetrieve import retrieveVsm
from whoosh.fields import Schema, TEXT, ID
import whoosh.index as index
from xml.dom import minidom

#files and directories
indexDir = "../data/index"
inputDir = "../csiro-corpus"
outputFile = "../output/baseline.out"
queriesFile = "../data/queries.xml"
temp = "testdocs"

handle = handle_html(temp)
print(handle[0])
print(handle[1])
print(handle[2])
print(handle[3])
#print(handle[4])

#print(handle)
"""
# Method for loading an xml file of queries
def loadQueries():
    queries = []
    xmldoc = minidom.parse(queriesFile)
    for query in xmldoc.getElementsByTagName("query"):
        queryId = query.getElementsByTagName("number")[0].firstChild.nodeValue
        text = query.getElementsByTagName("text")[0].firstChild.nodeValue
        queries.append({'id': queryId, 'text': text})

    return queries

# Creating the index. This calls the handle_html method that returns a dictionary with ID and content
# of each file under csiro-corpus
def createIndex():
    schema = Schema(id=ID(stored=True), content=TEXT)

    if not os.path.exists(indexDir):
        os.mkdir(indexDir)
    ix = index.create_in(indexDir, schema)

    writer = ix.writer()

    for doc in input_dir:
        docs = handle_html(doc)
        for doc in docs:
            writer.add_document(id=doc['id'].decode(),  content=doc['content'].decode())

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
        for docnum in sorted(res, key=res.get, reverse=True)[:10]:
            # Look up our docID
            stored = reader.stored_fields(docnum)
            # Write `docID Q0 queryID score` into `data/cacm.out`
            outfile.write(query['id']+ " Q0 " + stored['id'] + " " + str(res[docnum]) + "\n")

    outfile.close()
    ix.close()

if __name__ == '__main__':
    createIndex()  # note that this has to be done only once
    """
    #makeBaseline(indexDir, outputFile)
=======
from html_handler import handle_html

input_dir = "../csiro-corpus/CSIRO000"

handle = handle_html(input_dir)

print(handle)
>>>>>>> 53eb5cd1abe8a7d89b5f3436583f2c30cd90e86f

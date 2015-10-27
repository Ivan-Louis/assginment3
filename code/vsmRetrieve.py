from __future__ import division

import math
from collections import Counter
defaultField = "content"

def tfidf(reader, term, count, length):
    termFreq = count / length
    inverseDocFreq = math.log(reader.doc_count() / reader.doc_frequency(defaultField, term))
    return termFreq*inverseDocFreq


def retrieveVsm(reader, query):
    # Preprocess the query in a naive way
    qterms = query.split()
    qt = Counter(qterms)

    hits = {}
    docNorm = {}
    qNorm = 0
    for t, cnt in qt.items():

        if reader.frequency(defaultField, t) == 0:
            continue

        wtq = tfidf(reader, t, cnt, len(query.split()))
        qNorm += wtq * wtq
        pr = reader.postings(defaultField, t)
        while pr.is_active():
            docNum = pr.id()
            if docNum not in hits:
                hits[docNum] = 0
                docNorm[docNum] = 0
            freq = pr.value_as("frequency")
            docLen = reader.doc_field_length(docNum, defaultField)
            wtd = tfidf(reader, t, freq, docLen)
            hits[docNum] += wtq * wtd
            docNorm[docNum] += wtd * wtd
            pr.next()

    for docNum, score in hits.items():
        hits[(docNum)] = hits[docNum] / math.sqrt(qNorm * docNorm[docNum])

    return hits

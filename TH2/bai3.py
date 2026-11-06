import os
from whoosh.index import create_in
from whoosh.fields import *

titles = [
    "First document",
    "Second document",
    "Third document",
    "Fourth document",
    "Fifth document",
    "Sixth document",
    "Seventh document",
    "Eighth document",
    "Ninth document",
    "Tenth document"
]

contents = [
    "This document is about information retrieval.",
    "This document is about web search engines.",
    "This document explains the inverted index.",
    "This document is about document indexing.",
    "This document explains query processing.",
    "This document is about search results.",
    "This document explains information storage.",
    "This document is about text analysis.",
    "This document explains document ranking.",
    "This document is about digital libraries."
]

# path lưu mã tài liệu, title được lưu, content không được lưu.
schema = Schema(title=TEXT(stored=True), path=ID(stored=True),
                content=TEXT)

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

ix = create_in("indexdir", schema)
writer = ix.writer()

for i in range(10):
    writer.add_document(title=titles[i], path=str(i),
                        content=contents[i])

writer.commit()

from whoosh.qparser import QueryParser

query_string = input("Enter query: ")

with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse(query_string)
    results = searcher.search(query)

    print("Number of results:", len(results))
    for i in range(len(results)):
        print(i + 1, results[i]["title"])

    if len(results) > 0:
        number = int(input("Enter result number: "))
        document_id = int(results[number - 1]["path"])
        print(contents[document_id])

import os
from pyvi import ViTokenizer
from whoosh.index import create_in
from whoosh.fields import *

schema = Schema(title=TEXT(stored=True), path=ID(stored=True),
                content=TEXT)

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

ix = create_in("indexdir", schema)
writer = ix.writer()

writer.add_document(title="Đại học Thủy Lợi", path="/a",
                    content=ViTokenizer.tokenize(
                        "Đại học Thủy Lợi là một trường đại học tại Hà Nội."))
writer.add_document(title="Đại học Quốc gia Hà Nội", path="/b",
                    content=ViTokenizer.tokenize(
                        "Đại học Quốc gia Hà Nội có nhiều trường thành viên."))

writer.commit()

from whoosh.qparser import QueryParser

with ix.searcher() as searcher:
    query_string = ViTokenizer.tokenize("Thủy Lợi")
    query = QueryParser("content", ix.schema).parse(query_string)
    results = searcher.search(query)
    print("Number of results:", len(results))
    print(results[0]["title"])

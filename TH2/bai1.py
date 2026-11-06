import os
from whoosh.index import create_in 
from whoosh.fields import * 
# "stored=True" nghĩa là sẽ lưu trữ trường này trong chỉ mục; 
# kiểu trường "ID" nghĩa là không đánh chỉ mục trên trường này. 
schema = Schema(title=TEXT(stored=True), path=ID(stored=True),  
content=TEXT) 

# Tạo chỉ mục mới
if not os.path.exists("indexdir"): 
    os.mkdir("indexdir") # Tạo thư mục nếu nó chưa tồn tại 

# Đảm bảo thư mục "indexdir" tồn tại trong thư mục hiện hành trước  
# khi chạy câu lệnh bên dưới 
ix = create_in("indexdir", schema) 
writer = ix.writer() 
writer.add_document(title="First document", path="/a", 
content="This is the first document we've added!") 
writer.add_document(title="Second document", path="/b", 
content="The second one is even more interesting!") 
writer.commit() 
from whoosh.qparser import QueryParser 
with ix.searcher() as searcher: 
    query = QueryParser("content", ix.schema).parse("first") 
    results = searcher.search(query) 
    print("Number of results:", len(results)) 
    print(results[0]["title"]) 
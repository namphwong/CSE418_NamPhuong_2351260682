from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
 
# Mở chỉ mục đã xây dựng trước đây
ix = open_dir('indexdir')

# Yêu cầu người dùng nhập vào câu truy vấn
query_str = input('Enter a query: ')

# Chấm điểm các tài liệu theo số lần các từ truy vấn xuất hiện
# trong mỗi tài liệu (weighting=scoring.Frequency).
with ix.searcher(weighting=scoring.Frequency) as searcher:
    # Tìm kiếm trong trường content
    query = QueryParser('content', ix.schema).parse(query_str)
    results = searcher.search(query)
    
    # Số kết quả trả về
    num_results = len(results)
    
    if (num_results == 0):
        print('No results')
    else:	
        # Hiện các kết quả, mỗi dòng gồm số thứ tự, tiêu đề, điểm số
        for i in range(len(results)):
            print(i + 1, '-', results[i]['title'], '(' + str(results[i].score) + ')')
        
        # Yêu cầu người dùng chọn kết quả muốn xem chi tiết
        k = int(input('Which result do you want to show? '))
        
        # Mở và hiển thị nội dung file tương ứng với kết quả đã chọn
        fp = open(results[k - 1]['path'], 'r')
        print()
        print(fp.read())    
        fp.close()

from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir


# Mở chỉ mục đã xây dựng trước đây
ix = open_dir('indexdir')

# Nhập ba nhóm từ truy vấn
must_words = input('Enter words that must appear: ')
any_words = input('Enter words where at least one must appear: ')
not_words = input('Enter words that must not appear: ')

# Tạo câu truy vấn đầy đủ
query_parts = []

if must_words.strip():
    query_parts.append(must_words.strip())

if any_words.strip():
    query_parts.append('(' + ' OR '.join(any_words.split()) + ')')

for word in not_words.split():
    query_parts.append('NOT ' + word)

query_str = ' '.join(query_parts)
print('Full query:', query_str)

# Chấm điểm các tài liệu theo số lần các từ truy vấn xuất hiện
with ix.searcher(weighting=scoring.Frequency) as searcher:
    query = QueryParser('content', ix.schema).parse(query_str)
    results = searcher.search(query)

    num_results = len(results)

    if num_results == 0:
        print('No results')
    else:
        # Hiện số thứ tự, tên file, tiêu đề và điểm số
        for i in range(len(results)):
            print(i + 1, '-', results[i]['title'],
                  '(' + str(results[i].score) + ')')

        # Chọn và hiển thị nội dung tài liệu
        k = int(input('Which result do you want to show? '))

        fp = open(results[k - 1]['path'], 'r')
        print()
        print(fp.read())
        fp.close()

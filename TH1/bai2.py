from pyvi import ViTokenizer


document = input("Nhập tài liệu tiếng Việt: ")
query_word = input("Nhập từ cần tìm: ")

words = ViTokenizer.tokenize(document.lower()).split()
query_word = ViTokenizer.tokenize(query_word.lower())

if query_word in words:
    print("Từ có mặt trong tài liệu")
else:
    print("Từ không có mặt trong tài liệu")

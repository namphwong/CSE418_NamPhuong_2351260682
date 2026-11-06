import os
from pyvi import ViTokenizer


folder = "documents"
file_names = sorted(os.listdir(folder))
documents = []

# Đọc 10 file và lưu nội dung vào bộ nhớ.
for file_name in file_names:
    path = os.path.join(folder, file_name)
    f = open(path, "r", encoding="utf-8")
    documents.append(f.read())
    f.close()

# Tạo từ điển: từ -> danh sách số thứ tự tài liệu.
inverted_index = {}

for i in range(len(documents)):
    words = ViTokenizer.tokenize(documents[i].lower()).split()
    unique_words = []

    for word in words:
        if word not in unique_words:
            unique_words.append(word)

    for word in unique_words:
        if word not in inverted_index:
            inverted_index[word] = []
        inverted_index[word].append(i + 1)

# Tìm các tài liệu chứa từ truy vấn.
query = input("Nhập từ truy vấn: ")
query_words = ViTokenizer.tokenize(query.lower()).split()

result = []
if len(query_words) > 0:
    result = inverted_index.get(query_words[0], []).copy()

    for word in query_words[1:]:
        result = [doc_id for doc_id in result
                  if doc_id in inverted_index.get(word, [])]

print("Các tài liệu chứa từ truy vấn:", result)

for doc_id in result:
    print(doc_id, "-", file_names[doc_id - 1])

if len(result) > 0:
    selected = int(input("Chọn số thứ tự tài liệu: "))
    print(documents[selected - 1])

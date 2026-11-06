import nltk


document = input("Nhập tài liệu tiếng Anh: ")

words = nltk.word_tokenize(document)
stemmer = nltk.PorterStemmer()

print("Các từ sau khi tách:", words)
print("Các từ sau khi tách gốc:")

for word in words:
    print(word, "->", stemmer.stem(word))

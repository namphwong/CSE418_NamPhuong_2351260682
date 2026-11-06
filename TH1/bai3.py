from pyvi import ViTokenizer


document = input("Nhập tài liệu: ")
words = ViTokenizer.tokenize(document.lower()).split()

word_frequency = {}

for word in words:
    if word in word_frequency:
        word_frequency[word] += 1
    else:
        word_frequency[word] = 1

for word, frequency in word_frequency.items():
    print(word, ":", frequency)

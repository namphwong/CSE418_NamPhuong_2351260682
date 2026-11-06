from pyvi import ViTokenizer


# Tập tài liệu D được gõ trực tiếp trong code.
documents = [
    "Học máy giúp máy tính học từ dữ liệu",
    "Khoa học dữ liệu sử dụng thống kê và lập trình",
    "Python là ngôn ngữ lập trình phổ biến",
    "Trí tuệ nhân tạo có nhiều ứng dụng trong cuộc sống"
]

document_frequency = {}

for document in documents:
    words = ViTokenizer.tokenize(document.lower()).split()
    unique_words = []

    for word in words:
        if word not in unique_words:
            unique_words.append(word)

    for word in unique_words:
        if word in document_frequency:
            document_frequency[word] += 1
        else:
            document_frequency[word] = 1

for word, frequency in document_frequency.items():
    print(word, ":", frequency)

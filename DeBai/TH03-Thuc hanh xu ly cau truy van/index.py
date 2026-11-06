import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID

# Hàm tạo chỉ mục (root là tên thư mục chứa các tài liệu)
def createIndex(root):   
    # Định nghĩa lược đồ cho chỉ mục (không lưu trữ trường content)
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True),
                    content=TEXT)
    
    # Nếu thư mục chứa chỉ mục chưa tồn tại thì tạo ra
    if not os.path.exists('indexdir'):
        os.mkdir('indexdir')
 
    # Tạo chỉ mục
    ix = create_in('indexdir', schema)
    writer = ix.writer()
 
    # Lấy về đường dẫn tới các file tài liệu
    # (Tìm hiểu về "list comprehension" trong Python để hiểu cú pháp bên dưới)
    filepaths = [os.path.join(root, fn) for fn in os.listdir(root)]

    # Xử lý lần lượt từng file tài liệu
    for path in filepaths:
        # Mở file
        fp = open(path, 'r')
        print(path)
        
        # Đọc toàn bộ nội dung file rồi tách xâu dựa trên dấu xuống dòng đầu
        # tiên. Dòng đầu tiên là tiêu đề, phần còn lại là nội dung.
        text = fp.read().split('\n', 1) # 1 nghĩa là chỉ tách xâu 1 lần
        
        # Tiêu đề trong chỉ mục gồm tên file và tiêu đề tài liệu
        writer.add_document(title=path.split('\\')[1] + ' - ' + text[0],
                            path=path, content=text[1])
        
        # Đóng file
        fp.close()
    
    writer.commit() # Kết thúc ghi các tài liệu vào chỉ mục
    print('Finished')

# Tạo chỉ mục trên tập tài liệu nằm trong thư mục "CS-Docs"
createIndex('CS-Docs')

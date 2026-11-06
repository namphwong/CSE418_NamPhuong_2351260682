list1 = list(map(int, input("Nhập danh sách thứ nhất: ").split()))
list2 = list(map(int, input("Nhập danh sách thứ hai: ").split()))

intersection = []
union = []

for number in list1:
    if number in list2 and number not in intersection:
        intersection.append(number)

for number in list1 + list2:
    if number not in union:
        union.append(number)

intersection.sort()
union.sort()

print("Giao:", intersection)
print("Hợp:", union)

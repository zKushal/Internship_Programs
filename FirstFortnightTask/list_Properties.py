# List Properties

# 1. Lists are ordered
print("Ordered List:")
number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(number_list)
print(f"Length of the list: {len(number_list)}")
number_list[2]="Updated Value"
print(f"Updated List: {number_list}")

 
print("Mutable List:")
number_list[2] = 100
print(number_list)

# 3. Lists can contain duplicate values
print("List with Duplicates:")
number_list.append(100)
number_list.append(100)
number_list.append(1)
print(number_list)

# 4. Lists can contain different data types
print("Mixed Data Type List:")
mixed_list = [1, "Hello", 3.14, True]
print(mixed_list)

# 5. Lists can be nested
print("Nested List:")
nested_list = [1, [2, 3], [4, 5, 6]]
print(nested_list)

# Dynamic nature of lists
print("Dynamic List:")
dynamic_list = []
for i in range(10):
    dynamic_list.append(i)
    print(dynamic_list)
    
# Supports slicing and indexing
print("Slicing and Indexing:")
print(number_list[0:4])  # print between index 0 and 3
print(number_list[5])    # print element at index 5
print(number_list[-1])   # print last element i.e 1
print(number_list[-3:])  # print last three elements i.e [100, 100, 10]\


# Sorting and reversing
print("Sorting and Reversing:")
print("Original List:", number_list)
number_list.sort()
print("Sorted List:", number_list)
number_list.reverse()
print("Reversed List:", number_list)
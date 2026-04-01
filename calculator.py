# first = float(input("Enter the first number: "))
# second = float(input("Enter the second number: "))
# operation = input("Enter the operation (+, -, *, /): ")

# if operation == "+":
#     result = first + second
#     print("Sum:", result)
#
# elif operation == "-":
#     result = first - second
#     print("Difference:", result)
#
# elif operation == "*":
#     result = first * second
#     print("Product: ", result)
#
# elif operation == "/":
#     if second ==0:
#         print("Error: Division by zero is not allowed.")
#     else:
#         result = first / second
#         print("Division:", result)
# else:
#     print("Please enter a valid operation.")
#

def add(first, second):
    return first + second

def sub(first, second):
    return first - second

def div(first, second):
        return first / second

def mul(first, second):
    return first * second


while True:
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        operation = input("Enter the operation (+, -, *, /):")

        if operation == "+":
            print(num1 + num2)

        elif operation == "-":
            print(num1 - num2)

        elif operation == "*":
            print(num1*num2)

        elif operation == "/":
            if num2 == 0:
                print("Error: Division by zero")

            else:
                print(num1 / num2)
        else:
            print("Error: You entered invalid operation")

    finally:
        input("Press any key to continue...")
        continue





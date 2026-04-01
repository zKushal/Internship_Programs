# Calculator Using Class
class Calculator:
    
    def __init__(self, a, b): # self means the instance of the class, it allows us to access the attributes and methods of the class in python. It is a convention to use self as the first parameter of the method in a class, but you can use any name you like.
        self.a = a
        self.b = b
        
    def add(self):
        result = self.a + self.b
        print("Sum:", result)
        
    def sub (self):
        result = self.a - self.b
        print("Difference:", result)
        
    def mul(self):
        result = self.a *self.b
        print(f"Product: {result}") # f means format string, it allows us to embed expressions inside string literals, using curly braces {}. The expressions are evaluated at runtime and then formatted using the format() protocol.
        
    def div(self):
        if self.b == 0:
            print("Error: Not divisible by ZERO")
            
        else:
            result = self.a / self.b
            print(f"Division: {result}")

            
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number:"))
operation = input("Enter operation (+, -, *, /): ")

obj = Calculator(num1, num2)

if operation == "+":
    obj.add()
elif operation == "-":
    obj.sub()
elif operation == "*":
    obj.mul()
elif operation == "/":
    obj.div()
else:
    print("Invalid Operation")
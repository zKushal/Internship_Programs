class Person:
    global_first_name = ""
    global_last_name = ""
    global_age = 0
    
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        
        
person1 = Person("John", "Doe", 30)
person2 = Person("Jane", "Smith", 25)
person3 = Person("Alice", "Johnson", 35)
person4 = Person("Alice", "Johnson", 35)

people = [person1, person2, person3, person4] # object of class Person is stored in list people 

people_with_Alice = list(
    filter(
        lambda person: person.global_first_name == "Alice", people
        ))

for person in people_with_Alice:
    print(f"First Name: {person.global_first_name}, {person.global_last_name}, Age: {person.global_age}")
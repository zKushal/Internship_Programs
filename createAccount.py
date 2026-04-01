

class createAccount:
    createAccountList = []
    def __init__(self, first_name, last_name, age, address, phoneNumber, citizenshipNumber):
        self.global_first_name = first_name
        self.global_last_name = last_name
        self.global_age = age
        self.global_address = address
        self.global_phoneNumber = phoneNumber
        self.global_citizenshipNumber = citizenshipNumber
        createAccount.createAccountList.append(self)

    def displayAccountDetails(self):
        print(f"First Name: {self.global_first_name}")
        print(f"Last Name: {self.global_last_name}")
        print(f"Age: {self.global_age}")
        print(f"Address: {self.global_address}")
        print(f"Phone Number: {self.global_phoneNumber}")
        print(f"Citizenship Number: {self.global_citizenshipNumber}")
            
            
n = int(input("Enter the number of accounts you want to create: "))
            
for i in  (n):
    print(f"Enter details for account {i+1}:")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    age = int(input("Enter age: "))
    address = input("Enter address: ")
    phoneNumber = int(input("Enter phone number: "))
    citizenshipNumber = int(input("Enter citizenship number: "))
                
    print("Account created successfully!!!")
    print("\n")
    
         
    account = createAccount(first_name, last_name, age, address, phoneNumber, citizenshipNumber)
    
    createAccount.createAccountList.append(account)
    
search_citizenship_number = int(input("Enter citizenship number to search: "))
found_account = False

if search_citizenship_number == account.global_citizenshipNumber:
    print("Account found!!! Details are as follows: ")
    account.displayAccountDetails()
    found_account = True
    
else:
    print("Account not found.")
    
    
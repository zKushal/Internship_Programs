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
        
class BankAccount:
    def __init__(self):
        self.amount = 0
    
    def depositAmount(self, amount):
        if amount <= 0:
            print("Please enter valid amount")
        else:
            self.amount += amount
            print(f"Deposited Amount: {self.amount}")
            print("Amount Deposited Successfully")
    
    def withdrawAmount(self, amount):
        if self.amount <= 0:
            print("Please enter valid amount")
        elif amount > self.amount:
            print("Insufficient funds")
        else:
            self.amount -= amount
            print("Amount Withdrawn Successfully")
    
    def checkBalance(self):
        print(f"Your current balance is: {self.amount}")
        
        
obj = BankAccount()
while True:
  print("1. Create Account")
  print("2. Deposit Amount")
  print("3. Withdraw Amount") 
  print("4. Check Balance")
  print("5. View Account Details")
  print("6. Exit")  
  select = input("Please select an option (1-6): ")
  
  match select:
        
        case "1":
            n = int(input("Enter the number of accounts you want to create: "))
            
            for i in range(n):
                print("\n")
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
                
            search_citizenship_number = int(input("Enter citizenship number to search: "))
            found_account = False
            
            for account in createAccount.createAccountList:
                if search_citizenship_number == account.global_citizenshipNumber:
                    print("Account found!!! Details are as follows: ")
                    account.displayAccountDetails()
                    found_account = True
                    break
            if not found_account:
                print("Account not found.")
                print("\n")
        case "2":
            print("\n")
            deposit_amount = float(input("Enter the amount to deposit: "))
            obj.depositAmount(deposit_amount)
            obj.checkBalance()
            input("Press Enter to continue...")
            
        case "3":
            
            print("\n")
            withdraw_amount = float(input("Enter the amount to withdraw: "))
            obj.withdrawAmount(withdraw_amount)
            obj.checkBalance()
            input("Press Enter to continue...")

        case "4":
            obj.checkBalance()
            input("Press Enter to continue...")
   
        case "5":
            search_citizenship_number = int(input("Enter citizenship number to search: "))
            found_account = False
            for account in createAccount.createAccountList:
                if search_citizenship_number == account.global_citizenshipNumber:
                    print("Account found!!! Details are as follows: ")
                    account.displayAccountDetails()
                    found_account = True
                    break
            if not found_account:
                print("Account not found.")
            input("Press Enter to continue...")
        case "6":
            print("Thank you for using our banking services!")
            break
            
        case _:
            print("Invalid choice. Please try again.")
        
    
  
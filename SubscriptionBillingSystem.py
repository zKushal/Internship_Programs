from datetime import date

userDetailsList = []
subscriptionDetailsList = []
invoiceDetailsList = []


class UserDetails:
    def __init__(self, userId=0, name="", address="", age=0, email=""):
        self.userId = userId
        self.name = name
        self.address = address
        self.age = age
        self.email = email

    def enterUserDetails(self):
        self.userId = len(userDetailsList) + 1
        self.name = input("Enter your name: ")
        self.address = input("Enter your address: ")
        self.age = int(input("Enter your age: "))
        self.email = input("Enter your email: ")
        userDetailsList.append(self)

    def displayUserDetails(self):
        print("User ID\tName\tAddress\tAge\tEmail")
        print(f"{self.userId}\t{self.name}\t{self.address}\t{self.age}\t{self.email}")


class PlanDetails:
    def __init__(self):
        self.subscription_plans = {
            1: ("Basic", 1000),
            2: ("Standard", 5000),
            3: ("Premium", 10000),
        }

    def displayPlanDetails(self):
        
        print("\nAvailable Subscription Plans")
        print("Plan No\tPlan Name\tPrice")
        for planNum, (planName, planPrice) in self.subscription_plans.items():
            print(f"{planNum}\t\t{planName}\t\t{planPrice}")

    def getPlanBySelection(self, planNum):
        return self.subscription_plans.get(planNum, None)


class SubscriptionDetails:
    def __init__(self, userID=0, planName="", amount=0, status="Inactive"):
        self.subscriptionID = len(subscriptionDetailsList) + 1
        self.userID = userID
        self.planName = planName
        self.amount = amount
        self.startDate = str(date.today())
        self.status = status

        

    def displaySubscriptionDetails(self):
        print("Subscription ID\tUser ID\tPlan\tAmount\tStart Date\tStatus")
        print(
            f"{self.subscriptionID}\t\t{self.userID}\t{self.planName}\t{self.amount}\t{self.startDate}\t{self.status}"
        )


class InvoiceDetails:
    def __init__(self, invoiceId=0, userID=0, planName="", amount=0, payment=0):
        self.invoiceID = invoiceId
        self.userID = userID
        self.planName = planName
        self.amount = amount
        self.payment = payment
        self.change = payment - amount
        self.billingDate = str(date.today())

    def displayInvoiceDetails(self):
        print("\n----------- Invoice -----------")
        print(f"Invoice ID      : {self.invoiceID}")
        print(f"User ID         : {self.userID}")
        print(f"Plan            : {self.planName}")
        print(f"Plan Amount     : {self.amount}")
        print(f"Payment Received: {self.payment}")
        print(f"Change Returned : {self.change}")
        print(f"Billing Date    : {self.billingDate}")
        print("-------------------------------")


def searchUserbyID(userId):
    return next((searchId for searchId in userDetailsList if searchId.userId == userId), None)


def selectPlan_generateInvoice(userId):
    plan_details = PlanDetails()
    plan_details.displayPlanDetails()
    planNum = int(input("Select a plan number (1/2/3): "))
    selectedPlan = plan_details.getPlanBySelection(planNum)

    if not selectedPlan:
        print("Invalid plan selection.")
        return

    planName, amount = selectedPlan

    subscription = SubscriptionDetails(userID=userId, planName=planName, amount=amount, status="Pending Payment")
    subscriptionDetailsList.append(subscription)


    payment = int(input(f"Enter payment for {planName} plan (Amount: {amount}): "))
    if payment < amount:
        print("Insufficient payment. Invoice was not generated.")
        subscription.status = "Inactive"
        return

    subscription.status = "Active"

    invoice_id = len(invoiceDetailsList) + 1
    invoice = InvoiceDetails(invoiceId=invoice_id, userID=userId, planName=planName, amount=amount, payment=payment)
    invoiceDetailsList.append(invoice)
    invoice.displayInvoiceDetails()


while True:
    print("\nSubscription Billing System")
    print("1. Enter User Details")
    print("2. Display User Details")
    print("3. View Subscription Plans and Prices")
    print("4. Select Plan, Pay, and Generate Invoice")
    print("5. Display Subscription Details")
    print("6. Display Invoice Details")
    print("7. Exit")

    choice = int(input("Enter your choice: "))

    match choice:
        case 1:

            user = UserDetails()
            user.enterUserDetails()

        case 2:

            userID = int(input("Enter User ID to search: "))
            user = searchUserbyID(userID)
            if user:
                user.displayUserDetails()
            else:
                print("User not found.")

        case 3:
            planDetails = PlanDetails()
            planDetails.displayPlanDetails()

        case 4:

            user_id = int(input("Enter your User ID: "))
            user = searchUserbyID(user_id)
            if user:
                selectPlan_generateInvoice(user.userId)
            else:
                print("User not found. Please enter valid User ID.")

        case 5:

            search_user_id = int(input("Enter User ID to search: "))
            user = searchUserbyID(search_user_id)
            if user:
                print("\nSubscription Details:")
                userSubscription = [sub for sub in subscriptionDetailsList if sub.userID == search_user_id]
                if userSubscription:
                    for subscription in userSubscription:
                        subscription.displaySubscriptionDetails()
                else:
                    print("No subscriptions found for this user.")
            else:
                print("User not found.")

        case 6:

            search_user_id = int(input("Enter User ID to search: "))
            user = searchUserbyID(search_user_id)
            if user:
                print("\nInvoice Details:")
                user_invoices = [inv for inv in invoiceDetailsList if inv.userID == search_user_id]
                if user_invoices:
                    for invoice in user_invoices:
                        invoice.displayInvoiceDetails()
                else:
                    print("No invoices found for this user.")
            else:
                print("User not found.")

        case 7:

            print("Exiting the system. Goodbye!")
            break

        case _:

            print("Invalid choice. Please try again.")
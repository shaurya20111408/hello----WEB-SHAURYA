balance = 5000
amount = int(input("Enter your amount: "))
if (amount>5000):
    print("Insufficient balance")
elif (amount<=0):
    print("Enter valid amount")
else:
    balance -= amount
    print("Transaction successful. Your balance is:", balance)
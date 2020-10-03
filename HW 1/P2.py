balance = float(input("Enter outstanding balance: "))
annual_interest_rate = float(input("Enter annual interest rate: "))


def mini(bal, mon):
    for x in range(12):
        bal += bal*mon
    return bal/12.0
# def payment(monthly_payments, bala):
#     for x in range(12):
#         bal +=


monthly_interest_rate = annual_interest_rate/12
monthly = round(mini(balance, monthly_interest_rate), -1)
print(monthly)
i = 0
while balance > 0:
    balance = balance*(1+monthly_interest_rate)-monthly
    i += 1
print("RESULT")
print("Monthly payment to pay off debt in 1 year: ", monthly)
print("Months: ", i)
print("Balance: ", round(balance, 2))

ini_balance = float(input("Enter outstanding balance: "))
annual_interest_rate = float(input("Enter annual interest rate: "))

monthly_interest_rate = annual_interest_rate/12
balance = ini_balance

mon_pay_lower_bound = balance/12.0
mon_pay_upper_bound = (balance*(1+monthly_interest_rate)**12.0)/12.0
months = 0

while True:
    payment = (mon_pay_upper_bound + mon_pay_lower_bound) / 2
    balance = ini_balance
    while balance > 0 and months < 12:
        months += 1
        balance = round(balance * (1 + monthly_interest_rate), 2) - payment
    if abs(mon_pay_upper_bound - mon_pay_lower_bound) < 0.005:
        payment = round(payment + 0.00499999, 2)
        print("RESULT")
        print("Monthly payment to pay off debt in 1 year: ", payment)
        balance = ini_balance
        months = 0
        while balance > 0 and months < 12:
            months += 1
            balance = balance * (1 + monthly_interest_rate) - payment
        balance = round(balance, 2)
        print("Number of months needed: ", months)
        print("Balance: ", balance)
        break
    elif balance < 0:
        mon_pay_upper_bound = payment
    else:
        mon_pay_lower_bound = payment
    months = 0

# Problem 1
def remaining_balance(min_monthly_payment_rate, balance, ann):
    payment = round(min_monthly_payment_rate*balance, 2)
    interest_paid = round(ann / 12 * balance, 2)
    principal_paid = payment - interest_paid
    return balance - principal_paid, payment, principal_paid


bal = float(input("Enter the outstanding balance on your credit card: "))
annual_interest_rate = float(input("Enter the annual credit card interest rate as a decimal: "))
monthly_payment_rate = float(input("Enter the minimum monthly payment rate as a decimal: "))
total_amount_paid = 0

for x in range(12):
    remaining_bal, min_monthly, prin = remaining_balance(monthly_payment_rate, bal, annual_interest_rate)
    remaining_bal, min_monthly, prin = round(remaining_bal, 2), round(min_monthly, 2), round(prin, 2)
    print(f'Month: {x+1}')
    print(f'Minimum monthly payment: ${min_monthly}')
    print(f'Principle paid: ${prin}')
    print(f'Remaining balance: ${remaining_bal}')
    bal = remaining_bal
    total_amount_paid += min_monthly

print("RESULT")
print(f'Total amount paid: ${round(total_amount_paid, 2)}')
print(f'Remaining balance: ${bal}')
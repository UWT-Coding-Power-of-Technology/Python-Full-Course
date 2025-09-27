def calculate_due_amount(total_bill, amount_paid):
    return amount_paid - total_bill


bill = 2.50
paid = 4.00

due_amount = calculate_due_amount(bill, paid)
print("The shopkeeper should return:", due_amount, "dollars")

# Import the calendar module
import calendar

# Display all the month names
print("List of all months:\n")

# month_name is an array where index 1 = January, 12 = December
for month in calendar.month_name:
    if month:  # skips the empty string at index 0
        print(month)

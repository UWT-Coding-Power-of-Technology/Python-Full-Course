# Import both modules
import datetime
import calendar

# Step 1: Display current date and time
current_date_time = datetime.datetime.now()
print("Current Date and Time:", current_date_time)
print()

# Step 2: Display all the month names
print("List of all months:\n")
for month in calendar.month_name:
    if month:  # Skip empty string at index 0
        print(month)

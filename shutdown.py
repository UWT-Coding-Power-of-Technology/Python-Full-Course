def shutdown(input_value):
    if input_value.lower() == "yes":
        return "Shutting down"
    elif input_value.lower() == "no":
        return "Shutdown aborted"
    else:
        return "Sorry"

# Example calls:
print(shutdown("Yes"))   # Output: Shutting down
print(shutdown("no"))    # Output: Shutdown aborted
print(shutdown("maybe")) # Output: Sorry

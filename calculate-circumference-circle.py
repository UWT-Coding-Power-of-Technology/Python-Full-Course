import math

# Function to calculate circumference of a circle
def circumference(radius):
    return 2 * math.pi * radius

# Example usage
r = float(input("Enter the radius of the circle: "))
print("The circumference of the circle is:", circumference(r))

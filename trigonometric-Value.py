import math
import random

angle_deg = random.randint(0, 360)
angle_rad = math.radians(angle_deg)

sin_value = math.sin(angle_rad)
cos_value = math.cos(angle_rad)
try:
    tan_value = math.tan(angle_rad)
except:
    tan_value = "undefined (division by zero)"

# Display results
print(f"Random angle: {angle_deg}°")
print(f"sin({angle_deg}°) = {sin_value:.4f}")
print(f"cos({angle_deg}°) = {cos_value:.4f}")
print(f"tan({angle_deg}°) = {tan_value if isinstance(tan_value, str) else round(tan_value, 4)}")


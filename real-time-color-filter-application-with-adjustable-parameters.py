# If an error comes - Use Replit Agent for Rebuging error
# Real-Time RGB Filter for Replit
import cv2
import numpy as np

# --- Load your image ---
img = cv2.imread("image.jpg")  # Make sure your uploaded image is named "image.jpg"
if img is None:
    print("Failed to load image! Upload it to Replit and name it image.jpg")
    exit()

# Copy to modify
modified_img = img.copy()

# Channel intensities
red_intensity = 0
green_intensity = 0
blue_intensity = 0
step = 10  # Amount to increase/decrease

while True:
    # Apply intensity adjustments safely
    temp_img = modified_img.copy()
    temp_img[:, :, 2] = np.clip(temp_img[:, :, 2] + red_intensity, 0, 255)   # Red

    temp_img[:, :, 1] = np.clip(temp_img[:, :, 1] + green_intensity, 0, 255) # Green
    temp_img[:, :, 0] = np.clip(temp_img[:, :, 0] + blue_intensity, 0, 255)  # Blue

    # Display image
    cv2.imshow("RGB Filter", temp_img)

    # Wait for key press
    key = cv2.waitKey(0) & 0xFF

    # Quit
    if key == 27:  # ESC key
        break
    # Red channel
    elif key == ord('i'):
        red_intensity += step
    elif key == ord('k'):
        red_intensity -= step
    # Green channel
    elif key == ord('o'):
        green_intensity += step
    elif key == ord('l'):
        green_intensity -= step
    # Blue channel
    elif key == ord('f'):
        blue_intensity += step
    elif key == ord('d'):
        blue_intensity -= step
    # Save image
    elif key == ord('s'):
        save_name = input("Enter filename to save (with .png/.jpg): ")
        cv2.imwrite(save_name, temp_img)
        print(f"Saved as {save_name}")

cv2.destroyAllWindows()

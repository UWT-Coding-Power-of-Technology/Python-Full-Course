#Must use this in replit and ask agent to solve errors on port if file has errors
import cv2
import numpy as np

# ==========================
# Helper function
# ==========================
def nothing(x):
    pass

# ==========================
# Load Image
# ==========================
image_path = input("Enter path to your image: ")  # e.g., "image.jpg"
image = cv2.imread(image_path)
if image is None:
    print("Error: Image not found!")
    exit()

cv2.imshow("Original", image)

# Convert to grayscale for edge detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ==========================
# Create Trackbars
# ==========================
cv2.namedWindow("Parameters")

# Canny thresholds
cv2.createTrackbar("Canny Thresh1", "Parameters", 50, 255, nothing)
cv2.createTrackbar("Canny Thresh2", "Parameters", 150, 255, nothing)

# Sobel kernel size
cv2.createTrackbar("Sobel ksize", "Parameters", 3, 31, nothing)

# Laplacian kernel size
cv2.createTrackbar("Laplacian ksize", "Parameters", 3, 31, nothing)

# Gaussian filter kernel size
cv2.createTrackbar("Gaussian ksize", "Parameters", 3, 31, nothing)

# Median filter kernel size
cv2.createTrackbar("Median ksize", "Parameters", 3, 31, nothing)

# ==========================
# Main Loop
# ==========================
while True:
    # ---- Get trackbar positions ----
    canny1 = cv2.getTrackbarPos("Canny Thresh1", "Parameters")
    canny2 = cv2.getTrackbarPos("Canny Thresh2", "Parameters")
    sobel_ksize = cv2.getTrackbarPos("Sobel ksize", "Parameters")
    lap_ksize = cv2.getTrackbarPos("Laplacian ksize", "Parameters")
    gauss_ksize = cv2.getTrackbarPos("Gaussian ksize", "Parameters")
    median_ksize = cv2.getTrackbarPos("Median ksize", "Parameters")

    # Make sure kernel sizes are odd and at least 1
    sobel_ksize = max(1, sobel_ksize | 1)
    lap_ksize = max(1, lap_ksize | 1)
    gauss_ksize = max(1, gauss_ksize | 1)
    median_ksize = max(1, median_ksize | 1)

    # ---- Edge Detection ----
    canny_edges = cv2.Canny(gray, canny1, canny2)

    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_ksize)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_ksize)
    sobel_edges = cv2.magnitude(sobelx, sobely)
    sobel_edges = np.uint8(np.clip(sobel_edges, 0, 255))

    laplacian_edges = cv2.Laplacian(gray, cv2.CV_64F, ksize=lap_ksize)
    laplacian_edges = np.uint8(np.clip(laplacian_edges, 0, 255))

    # ---- Filtering ----
    gaussian_blur = cv2.GaussianBlur(image, (gauss_ksize, gauss_ksize), sigmaX=0)
    median_blur = cv2.medianBlur(image, median_ksize)

    # ---- Display results ----
    cv2.imshow("Canny", canny_edges)
    cv2.imshow("Sobel", sobel_edges)
    cv2.imshow("Laplacian", laplacian_edges)
    cv2.imshow("Gaussian Blur", gaussian_blur)
    cv2.imshow("Median Blur", median_blur)

    # Exit loop when ESC is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break

cv2.destroyAllWindows()

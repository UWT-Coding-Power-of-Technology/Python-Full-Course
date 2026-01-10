import cv2

# Load image
img = cv2.imread("image.jpg")

# Get image dimensions
height, width, _ = img.shape

# Arrow position
y = height - 40
start_point = (20, y)
end_point = (width - 20, y)

# Draw bi-directional arrows
color = (0, 255, 0)
thickness = 2
tip = 0.03

cv2.arrowedLine(img, start_point, end_point, color, thickness, tipLength=tip)
cv2.arrowedLine(img, end_point, start_point, color, thickness, tipLength=tip)

# Add width text
text = f"Width: {width}px"
text_x = width // 2 - 80
text_y = y - 10

cv2.putText(
    img,
    text,
    (text_x, text_y),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    color,
    2
)

# Show image
cv2.imshow("Image Width Annotation", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

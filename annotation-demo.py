import cv2
import numpy as np
import matplotlib.pyplot as plt

def create_annotated_image():
    # 1. Create a blank image (dark grey background)
    image = np.full((600, 800, 3), 40, dtype=np.uint8)
    
    # Define colors (BGR for OpenCV)
    COLORS = {
        'blue': (255, 100, 0),
        'green': (0, 255, 0),
        'red': (0, 0, 255),
        'yellow': (0, 255, 255),
        'white': (255, 255, 255),
        'cyan': (255, 255, 0)
    }

    # 2. Annotate with Shapes
    # Rectangle (Object detection style)
    cv2.rectangle(image, (50, 50), (250, 250), COLORS['green'], 3)
    cv2.putText(image, "Rectangle: Object A", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLORS['green'], 2)

    # Circle (Key point highlight)
    cv2.circle(image, (400, 150), 70, COLORS['blue'], -1) # Filled circle
    cv2.circle(image, (400, 150), 75, COLORS['white'], 2) # Border
    cv2.putText(image, "Circle: Key Region", (330, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLORS['white'], 2)

    # Lines (Connectivity/Path)
    cv2.line(image, (550, 50), (750, 250), COLORS['yellow'], 4)
    cv2.putText(image, "Line: Vector Path", (550, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLORS['yellow'], 2)

    # 3. Informative Text Labels
    cv2.putText(image, "Annotation Analysis Dashboard", (200, 550), cv2.FONT_HERSHEY_COMPLEX, 1, COLORS['cyan'], 2)

    # 4. Bi-directional Arrows and Measurements
    # Horizontal measurement
    cv2.arrowedLine(image, (50, 350), (250, 350), COLORS['red'], 2, tipLength=0.1)
    cv2.arrowedLine(image, (250, 350), (50, 350), COLORS['red'], 2, tipLength=0.1)
    cv2.putText(image, "Width: 200px", (90, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS['red'], 1)

    # Vertical measurement
    cv2.arrowedLine(image, (300, 50), (300, 250), COLORS['red'], 2, tipLength=0.1)
    cv2.arrowedLine(image, (300, 250), (300, 50), COLORS['red'], 2, tipLength=0.1)
    cv2.putText(image, "Height: 200px", (310, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS['red'], 1)

    # 5. Save the result
    # Convert BGR to RGB for Matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(10, 7))
    plt.imshow(image_rgb)
    plt.title("OpenCV Image Annotation Demonstration")
    plt.axis('off')
    
    # Save to a file for the user to see
    output_path = 'public/annotated_sample.png'
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1)
    print(f"Annotated image saved to {output_path}")

if __name__ == "__main__":
    create_annotated_image()

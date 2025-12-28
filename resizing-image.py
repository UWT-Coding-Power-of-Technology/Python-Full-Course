import cv2
import numpy as np
from flask import Flask, render_template_string

import base64
from io import BytesIO

app = Flask(__name__)

def create_test_image():
    """Creates a simple test image."""
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    cv2.rectangle(img, (100, 100), (700, 580), (0, 255, 0), 3)
    cv2.putText(img, "Test Image", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    return img

def image_to_base64(img):
    """Converts an OpenCV image to base64 for display in HTML."""
    buffer = cv2.imencode('.jpg', img)[1]
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64

@app.route('/')
def index():
    # Create the original image
    img = create_test_image()
    original_h, original_w = img.shape[:2]
    original_base64 = image_to_base64(img)

    # Resize the image to a smaller size
    resized_img = cv2.resize(img, (400, 300))
    resized_h, resized_w = resized_img.shape[:2]
    resized_base64 = image_to_base64(resized_img)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Processing</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}

            h1 {{
                color: #333;
            }}

            .container {{
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }}

            .image-box {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
        </style>
    </head>
    <body>
        <h1>Image Processing Output</h1>

        <div class="container">
            <div class="image-box">
                <h2>Original Image</h2>
                <p>Width: {{original_w}} px | Height: {{original_h}} px</p>
                <img src="data:image/jpeg;base64,{{original_base64}}" width="400"/>
            </div>

            <div class="image-box">
                <h2>Resized Image</h2>
                <p>Width: {{resized_w}} px | Height: {{resized_h}} px</p>
                <img src="data:image/jpeg;base64,{{resized_base64}}" width="400"/>
            </div>
        </div>
    </body>
    </html>
    """

    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

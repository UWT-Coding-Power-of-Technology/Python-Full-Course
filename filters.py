import cv2
import numpy as np
from flask import Flask, render_template_string
import base64
import os
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

def create_test_image():
    """Creates a simple test image with text and shapes for editing."""
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    cv2.rectangle(img, (10, 10), (790, 590), (0, 0, 0), 2)
    cv2.circle(img, (400, 300), 100, (255, 0, 0), -1)
    cv2.putText(img, "Photography Portfolio", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    cv2.putText(img, "Main Subject", (320, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return img

def image_to_base64(img):
    """Converts an OpenCV image to base64 for display in HTML."""
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    buffer = cv2.imencode('.jpg', img)[1]
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64

def apply_color_filter(image, filter_type):
    """Apply the specified color filter to the image."""
    filtered_image = image.copy()
    if filter_type == "red_tint":
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 0] = 0
    elif filter_type == "blue_tint":
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 2] = 0
    elif filter_type == "green_tint":
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 2] = 0
    elif filter_type == "increase_red":
        filtered_image[:, :, 2] = np.clip(filtered_image[:, :, 2] * 1.5, 0, 255)
    elif filter_type == "decrease_red":
        filtered_image[:, :, 2] = np.clip(filtered_image[:, :, 2] * 0.5, 0, 255)
    return filtered_image

@app.route('/')
def index():
    img = create_test_image()
    
    # Apply standard tints
    red_tint = apply_color_filter(img, "red_tint")
    blue_tint = apply_color_filter(img, "blue_tint")
    green_tint = apply_color_filter(img, "green_tint")
    more_red = apply_color_filter(img, "increase_red")
    less_red = apply_color_filter(img, "decrease_red")

    # Edge Detection & Filters
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 100, 200)
    gaussian_blur = cv2.GaussianBlur(img, (15, 15), 0)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Advanced Image Studio</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; max-width: 1400px; margin: 0 auto; padding: 30px; background: #121212; color: #e0e0e0; }}
            h1 {{ color: #4CAF50; text-align: center; border-bottom: 2px solid #333; padding-bottom: 15px; }}
            .section-title {{ color: #81c784; margin-top: 40px; border-left: 4px solid #4CAF50; padding-left: 15px; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            .card {{ background: #1e1e1e; padding: 15px; border-radius: 12px; border: 1px solid #333; }}
            h3 {{ font-size: 14px; margin-bottom: 10px; color: #4CAF50; }}
            img {{ width: 100%; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <h1>🎨 Advanced Image Processing Studio</h1>

        <h2 class="section-title">Color Tints & Adjustments</h2>
        <div class="grid">
            <div class="card"><h3>Original</h3><img src="data:image/jpeg;base64,{image_to_base64(img)}"></div>
            <div class="card"><h3>Red Tint</h3><img src="data:image/jpeg;base64,{image_to_base64(red_tint)}"></div>
            <div class="card"><h3>Blue Tint</h3><img src="data:image/jpeg;base64,{image_to_base64(blue_tint)}"></div>
            <div class="card"><h3>Green Tint</h3><img src="data:image/jpeg;base64,{image_to_base64(green_tint)}"></div>
            <div class="card"><h3>Increase Red</h3><img src="data:image/jpeg;base64,{image_to_base64(more_red)}"></div>
            <div class="card"><h3>Decrease Red</h3><img src="data:image/jpeg;base64,{image_to_base64(less_red)}"></div>
        </div>

        <h2 class="section-title">Computer Vision & Filters</h2>
        <div class="grid">
            <div class="card"><h3>Canny Edges</h3><img src="data:image/jpeg;base64,{image_to_base64(canny)}"></div>
            <div class="card"><h3>Gaussian Blur</h3><img src="data:image/jpeg;base64,{image_to_base64(gaussian_blur)}"></div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

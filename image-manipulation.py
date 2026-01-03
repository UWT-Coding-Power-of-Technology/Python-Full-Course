import cv2
import numpy as np
from flask import Flask, render_template_string
import base64
from io import BytesIO
import pytesseract
from PIL import Image
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

def create_test_image():
    """Creates a simple test image with text and shapes for editing."""
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    # Add a border
    cv2.rectangle(img, (10, 10), (790, 590), (0, 0, 0), 2)
    # Add a main subject to crop (a blue circle in the middle)
    cv2.circle(img, (400, 300), 100, (255, 0, 0), -1)
    # Add some text
    cv2.putText(img, "Photography Portfolio", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    cv2.putText(img, "Main Subject", (320, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return img

def image_to_base64(img):
    """Converts an OpenCV image to base64 for display in HTML."""
    buffer = cv2.imencode('.jpg', img)[1]
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64

def extract_text_from_image(img):
    """Extracts text from image using OCR (Tesseract)."""
    try:
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_img)
        extracted_text = pytesseract.image_to_string(pil_img)
        return extracted_text if extracted_text.strip() else "No text detected"
    except Exception as e:
        return f"Error: {str(e)}"

def save_images(images_dict):
    """Saves images to disk in a structured folder."""
    try:
        output_dir = "portfolio_output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for name, img in images_dict.items():
            cv2.imwrite(os.path.join(output_dir, f"{name}.jpg"), img)
        return "Portfolio images saved to 'portfolio_output' folder"
    except Exception as e:
        return f"Error saving: {str(e)}"

@app.route('/')
def index():
    # 1. Load Original
    img = create_test_image()
    original_base64 = image_to_base64(img)

    # 2. Rotate (Align) - 15 degrees
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 15, 1.0)
    rotated_img = cv2.warpAffine(img, M, (w, h), borderValue=(255,255,255))
    rotated_base64 = image_to_base64(rotated_img)

    # 3. Brighten (Vibrant Look) - Add 60
    brighter_img = cv2.convertScaleAbs(img, alpha=1.2, beta=60)
    brighter_base64 = image_to_base64(brighter_img)

    # 4. Crop (Highlight Main Subject) - Region around the blue circle
    crop_x, crop_y, crop_w, crop_h = 275, 175, 250, 250
    cropped_img = img[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    cropped_base64 = image_to_base64(cropped_img)

    # Save portfolio
    save_status = save_images({
        "1_original": img,
        "2_rotated": rotated_img,
        "3_brightened": brighter_img,
        "4_cropped": cropped_img
    })

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Photography Portfolio Editor</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 1200px; margin: 0 auto; padding: 30px; background-color: #1a1a1a; color: #eee; }}
            h1 {{ color: #4CAF50; text-align: center; border-bottom: 2px solid #333; padding-bottom: 15px; }}
            .status {{ background: #2e7d32; padding: 10px; margin-bottom: 20px; border-radius: 5px; text-align: center; font-weight: bold; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 30px; }}
            .card {{ background: #2d2d2d; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
            h2 {{ color: #81c784; font-size: 20px; margin-top: 0; }}
            p {{ font-size: 14px; color: #aaa; line-height: 1.6; }}
            img {{ width: 100%; border-radius: 8px; border: 1px solid #444; margin: 15px 0; }}
            .badge {{ display: inline-block; padding: 4px 8px; background: #444; border-radius: 4px; font-size: 12px; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <h1>📸 Photography Portfolio Editor</h1>
        <div class="status">✅ {save_status}</div>

        <div class="grid">
            <div class="card">
                <span class="badge">Step 1: Original</span>
                <h2>Raw Capture</h2>
                <p>The base image before any professional transformations.</p>
                <img src="data:image/jpeg;base64,{original_base64}">
            </div>

            <div class="card">
                <span class="badge">Step 2: Alignment</span>
                <h2>Rotated Image</h2>
                <p>Aligned the perspective by rotating 15 degrees for a dynamic look.</p>
                <img src="data:image/jpeg;base64,{rotated_base64}">
            </div>

            <div class="card">
                <span class="badge">Step 3: Color Correction</span>
                <h2>Vibrant Glow</h2>
                <p>Enhanced brightness and contrast to make the colors pop.</p>
                <img src="data:image/jpeg;base64,{brighter_base64}">
            </div>

            <div class="card">
                <span class="badge">Step 4: Focus</span>
                <h2>Subject Highlight</h2>
                <p>Cropped the image to focus directly on the primary subject.</p>
                <img src="data:image/jpeg;base64,{cropped_base64}">
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

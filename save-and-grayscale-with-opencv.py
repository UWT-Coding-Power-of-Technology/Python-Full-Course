import cv2
import numpy as np
from flask import Flask, render_template_string
import base64
from io import BytesIO
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

def create_test_image():
    """Creates a simple test image with text."""
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    cv2.rectangle(img, (100, 100), (700, 580), (0, 255, 0), 3)
    cv2.putText(img, "Test Image", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
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
        return extracted_text if extracted_text.strip() else "No text detected in image"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def save_images(original_img, resized_img, grayscale_img, resized_grayscale_img):
    """Saves images to disk."""
    try:
        output_dir = "processed_images"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        cv2.imwrite(os.path.join(output_dir, "original.jpg"), original_img)
        cv2.imwrite(os.path.join(output_dir, "resized.jpg"), resized_img)
        cv2.imwrite(os.path.join(output_dir, "original_grayscale.jpg"), grayscale_img)
        cv2.imwrite(os.path.join(output_dir, "resized_grayscale.jpg"), resized_grayscale_img)
        return "Images saved successfully in 'processed_images' folder"
    except Exception as e:
        return f"Error saving images: {str(e)}"

@app.route('/')
def index():
    # Create the original image
    img = create_test_image()
    original_h, original_w = img.shape[:2]
    original_base64 = image_to_base64(img)
    original_text = extract_text_from_image(img)
    
    # Convert to grayscale
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayscale_base64 = image_to_base64(cv2.cvtColor(grayscale_img, cv2.COLOR_GRAY2BGR))
    grayscale_text = extract_text_from_image(grayscale_img if len(grayscale_img.shape) == 2 else cv2.cvtColor(grayscale_img, cv2.COLOR_GRAY2BGR))

    # Resize the image to a smaller size
    resized_img = cv2.resize(img, (400, 300))
    resized_h, resized_w = resized_img.shape[:2]
    resized_base64 = image_to_base64(resized_img)
    resized_text = extract_text_from_image(resized_img)
    
    # Resize grayscale image
    resized_grayscale_img = cv2.resize(grayscale_img, (400, 300))
    resized_grayscale_base64 = image_to_base64(cv2.cvtColor(resized_grayscale_img, cv2.COLOR_GRAY2BGR))
    resized_grayscale_text = extract_text_from_image(cv2.cvtColor(resized_grayscale_img, cv2.COLOR_GRAY2BGR))
    
    # Save all images
    save_status = save_images(img, resized_img, grayscale_img, resized_grayscale_img)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Processing with Grayscale & OCR</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}

            h1 {{
                color: #333;
                text-align: center;
            }}
            
            .save-status {{
                background: #e8f5e9;
                border-left: 4px solid #4CAF50;
                padding: 12px;
                margin-bottom: 20px;
                border-radius: 4px;
                color: #2e7d32;
            }}

            .container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }}

            .image-box {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            
            .image-box h2 {{
                margin-top: 0;
                color: #333;
                font-size: 18px;
            }}
            
            .image-box p {{
                margin: 8px 0;
                font-size: 14px;
                color: #666;
            }}
            
            img {{
                width: 100%;
                max-width: 400px;
                height: auto;
                border-radius: 4px;
                margin: 10px 0;
            }}
            
            .text-box {{
                background: #f0f0f0;
                padding: 10px;
                border-radius: 4px;
                margin-top: 10px;
                border-left: 3px solid #4CAF50;
                font-family: monospace;
                font-size: 12px;
                max-height: 80px;
                overflow-y: auto;
                white-space: pre-wrap;
                word-break: break-all;
            }}
        </style>
    </head>
    <body>
        <h1>Image Processing with Grayscale & Text Extraction</h1>
        <div class="save-status">✅ {save_status}</div>

        <div class="container">
            <div class="image-box">
                <h2>Original Image</h2>
                <p>Width: {original_w} px | Height: {original_h} px</p>
                <img src="data:image/jpeg;base64,{original_base64}" alt="Original"/>
                <h3>Extracted Text:</h3>
                <div class="text-box">{original_text}</div>
            </div>

            <div class="image-box">
                <h2>Original Grayscale</h2>
                <p>Width: {original_w} px | Height: {original_h} px</p>
                <img src="data:image/jpeg;base64,{grayscale_base64}" alt="Grayscale"/>
                <h3>Extracted Text:</h3>
                <div class="text-box">{grayscale_text}</div>
            </div>

            <div class="image-box">
                <h2>Resized Image</h2>
                <p>Width: {resized_w} px | Height: {resized_h} px</p>
                <img src="data:image/jpeg;base64,{resized_base64}" alt="Resized"/>
                <h3>Extracted Text:</h3>
                <div class="text-box">{resized_text}</div>
            </div>

            <div class="image-box">
                <h2>Resized Grayscale</h2>
                <p>Width: {resized_w} px | Height: {resized_h} px</p>
                <img src="data:image/jpeg;base64,{resized_grayscale_base64}" alt="Resized Grayscale"/>
                <h3>Extracted Text:</h3>
                <div class="text-box">{resized_grayscale_text}</div>
            </div>
        </div>
    </body>
    </html>
    """

    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

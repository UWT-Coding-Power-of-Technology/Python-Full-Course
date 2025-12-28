import cv2
import numpy as np
from flask import Flask, render_template_string
import base64

app = Flask(__name__)

def create_test_image():
    """Create a simple test image with rectangle and text."""
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    cv2.rectangle(img, (100, 100), (700, 500), (0, 255, 0), 3)
    cv2.putText(img, "Test Image", (200, 320), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    return img

def image_to_base64(img):
    """Convert OpenCV image to base64 for HTML display."""
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')

@app.route('/')
def index():
    # Original image
    img = create_test_image()
    original_h, original_w = img.shape[:2]
    original_b64 = image_to_base64(img)

    # Three predefined sizes
    sizes = [(300, 300), (600, 400), (1200, 800)]
    resized_images = []
    for w, h in sizes:
        r = cv2.resize(img, (w, h))
        resized_images.append({
            "width": w,
            "height": h,
            "b64": image_to_base64(r)
        })

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Resizer</title>
        <style>
            body { font-family: Arial; background: #f5f5f5; padding: 20px; }
            .container { display: flex; flex-wrap: wrap; gap: 20px; }
            .image-box { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
            img { max-width: 100%; border-radius: 6px; }
        </style>
    </head>
    <body>
        <h1>Image Resizer Output</h1>
        <div class="container">
            <div class="image-box">
                <h2>Original Image</h2>
                <p>{{original_w}} x {{original_h}} px</p>
                <img src="data:image/jpeg;base64,{{original_b64}}">
            </div>
            {% for r in resized_images %}
            <div class="image-box">
                <h2>Resized Image</h2>
                <p>{{r.width}} x {{r.height}} px</p>
                <img src="data:image/jpeg;base64,{{r.b64}}">
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html,
                                  original_w=original_w,
                                  original_h=original_h,
                                  original_b64=original_b64,
                                  resized_images=resized_images)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

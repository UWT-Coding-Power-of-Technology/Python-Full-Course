import cv2
import numpy as np
from flask import Flask, render_template_string, request, jsonify
import base64
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'real_time_color_filter_project/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def create_test_image():
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    cv2.rectangle(img, (50, 50), (750, 550), (200, 200, 200), -1)
    cv2.putText(img, "Upload an Image to Start", (150, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (50, 50, 50), 2)
    return img

def image_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')

def apply_filter(image, ftype):
    """Apply a filter to the image based on the filter type."""
    img = image.copy()
    if ftype == "red_tint":
        img[:, :, 1] = img[:, :, 0] = 0
    elif ftype == "green_tint":
        img[:, :, 0] = img[:, :, 2] = 0
    elif ftype == "blue_tint":
        img[:, :, 1] = img[:, :, 2] = 0
    elif ftype == "sepia":
        img = np.array(image, copy=True)
        img = cv2.transform(img, np.matrix([[0.272, 0.534, 0.131],
                                            [0.349, 0.686, 0.168],
                                            [0.393, 0.769, 0.189]]))
        img = np.clip(img, 0, 255).astype(np.uint8)
    elif ftype == "cyan":
        img[:, :, 2] = 0 # Remove Red
    elif ftype == "magenta":
        img[:, :, 1] = 0 # Remove Green
    elif ftype == "sobel":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        # Using magnitude instead of bitwise_or for better Sobel results
        mag = cv2.magnitude(sx, sy)
        img_gray = np.uint8(np.clip(mag, 0, 255))
        img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    elif ftype == "canny":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        can = cv2.Canny(gray, 100, 200)
        img = cv2.cvtColor(can, cv2.COLOR_GRAY2BGR)
    elif ftype == "cartoon":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
            9, 9
        )
        color = cv2.bilateralFilter(image, 9, 300, 300)
        img = cv2.bitwise_and(color, color, mask=edges)
    return img

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real-Time Image Filters</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #121212; color: #e0e0e0; max-width: 1000px; margin: 0 auto; padding: 20px; }
            .container { background: #1e1e1e; padding: 30px; border-radius: 15px; box-shadow: 0 8px 32px rgba(0,0,0,0.5); }
            h1 { color: #4CAF50; text-align: center; }
            .controls { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 20px; }
            .preview-area { text-align: center; margin-top: 30px; }
            #preview { max-width: 100%; border-radius: 10px; border: 2px solid #333; }
            .btn { background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; transition: 0.3s; }
            .btn:hover { background: #45a049; }
            .btn.active { background: #2e7d32; border: 2px solid #fff; }
            .upload-section { margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 20px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎨 Real-Time Image Filters</h1>
            <div class="upload-section">
                <input type="file" id="fileInput" accept="image/*" class="btn">
                <button onclick="uploadImage()" class="btn">Load Image</button>
            </div>
            <div class="controls">
                <button onclick="setFilter('original')" class="btn">Original</button>
                <button onclick="setFilter('red_tint')" class="btn">Red Tint</button>
                <button onclick="setFilter('green_tint')" class="btn">Green Tint</button>
                <button onclick="setFilter('blue_tint')" class="btn">Blue Tint</button>
                <button onclick="setFilter('sepia')" class="btn">Sepia</button>
                <button onclick="setFilter('cyan')" class="btn">Cyan</button>
                <button onclick="setFilter('magenta')" class="btn">Magenta</button>
                <button onclick="setFilter('sobel')" class="btn">Sobel</button>
                <button onclick="setFilter('canny')" class="btn">Canny</button>
                <button onclick="setFilter('cartoon')" class="btn">Cartoon</button>
            </div>
            <div class="preview-area">
                <img id="preview" src="/placeholder">
            </div>
        </div>
        <script>
            let currentFilter = 'original';
            async function uploadImage() {
                const file = document.getElementById('fileInput').files[0];
                if (!file) return;
                const formData = new FormData();
                formData.append('file', file);
                const resp = await fetch('/upload', { method: 'POST', body: formData });
                const data = await resp.json();
                document.getElementById('preview').src = 'data:image/jpeg;base64,' + data.image;
                updateFilters();
            }
            async function setFilter(ftype) {
                currentFilter = ftype;
                updateFilters();
            }
            async function updateFilters() {
                const resp = await fetch('/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ftype: currentFilter })
                });
                const data = await resp.json();
                document.getElementById('preview').src = 'data:image/jpeg;base64,' + data.image;
            }
        </script>
    </body>
    </html>
    """)

@app.route('/placeholder')
def placeholder():
    img = create_test_image()
    return f"data:image/jpeg;base64,{image_to_base64(img)}"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, 'current.jpg')
    file.save(path)
    img = cv2.imread(path)
    return jsonify({'image': image_to_base64(img)})

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    path = os.path.join(UPLOAD_FOLDER, 'current.jpg')
    img = cv2.imread(path) if os.path.exists(path) else create_test_image()
    if img is None: img = create_test_image()
    filtered = apply_filter(img, data.get('ftype', 'original'))
    return jsonify({'image': image_to_base64(filtered)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

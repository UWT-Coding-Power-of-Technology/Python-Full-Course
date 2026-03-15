// If this hand detetion does not work - try asking a AI such as Chatgpt, Agent 4 Replit, grok, microsoft coplit, Gemini, claude and maybe more ai
import  cv2
import numpy as np
from flask import Flask, render_template_string, request, jsonify
import base64
import os

try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except (ImportError, AttributeError):
    HAS_MEDIAPIPE = False

app = Flask(__name__)

UPLOAD_FOLDER = 'real_time_color_filter_project/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if HAS_MEDIAPIPE:
    try:
        mp_hands = mp.solutions.hands
        # Lower confidence to 0.3 for better real-time detection
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3
        )
        mp_draw = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
    except AttributeError:
        HAS_MEDIAPIPE = False

def image_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buffer).decode('utf-8')

def detect_gesture(landmarks, handedness):
    fingers = []
    tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    for tip in tips:
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
            fingers.append(1)
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    if (handedness == "Right" and thumb_tip.x > thumb_ip.x) or \
       (handedness == "Left" and thumb_tip.x < thumb_ip.x):
        fingers.append(1)
    total = sum(fingers)
    if total == 5:
        return "Open Palm - SCROLL UP"
    elif total == 0:
        return "Fist - SCROLL DOWN"
    else:
        return f"Partial ({total} fingers)"

def process_frame(image, ftype):
    img = image.copy()
    h, w = img.shape[:2]
    gesture_msg = "No hand detected"
    detected = False

    if HAS_MEDIAPIPE:
        # Upscale small frames for better detection
        scale = 1.5 if w < 400 else 1.0
        proc = cv2.resize(img, (int(w * scale), int(h * scale))) if scale > 1 else img

        # Improve contrast before detection
        lab = cv2.cvtColor(proc, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        proc = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)

        img_rgb = cv2.cvtColor(proc, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks and results.multi_handedness:
            detected = True
            msgs = []
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                label = results.multi_handedness[i].classification[0].label

                # Scale landmarks back to original image size
                if scale > 1:
                    for lm in hand_landmarks.landmark:
                        lm.x = lm.x  # already normalized 0-1, no need to scale back
                
                mp_draw.draw_landmarks(
                    img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
                )

                lm = hand_landmarks.landmark
                th = mp_hands.HandLandmark.THUMB_TIP
                ix = mp_hands.HandLandmark.INDEX_FINGER_TIP
                tp = (int(lm[th].x * w), int(lm[th].y * h))
                ip = (int(lm[ix].x * w), int(lm[ix].y * h))
                cv2.circle(img, tp, 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, ip, 10, (255, 0, 0), cv2.FILLED)
                cv2.line(img, tp, ip, (0, 255, 255), 2)

                gesture = detect_gesture(hand_landmarks, label)
                msgs.append(f"{label}: {gesture}")
            gesture_msg = " | ".join(msgs)

    # Apply color filter
    if ftype == "red_tint":
        img[:, :, 1] = img[:, :, 0] = 0
    elif ftype == "green_tint":
        img[:, :, 0] = img[:, :, 2] = 0
    elif ftype == "blue_tint":
        img[:, :, 1] = img[:, :, 2] = 0
    elif ftype == "sepia":
        s = cv2.transform(np.array(img, copy=True), np.matrix([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]
        ]))
        img = np.clip(s, 0, 255).astype(np.uint8)
    elif ftype == "cyan":
        img[:, :, 2] = 0
    elif ftype == "magenta":
        img[:, :, 1] = 0
    elif ftype == "sobel":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        img = cv2.cvtColor(np.uint8(np.clip(cv2.magnitude(sx, sy), 0, 255)), cv2.COLOR_GRAY2BGR)
    elif ftype == "canny":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(cv2.Canny(gray, 100, 200), cv2.COLOR_GRAY2BGR)
    elif ftype == "cartoon":
        gray = cv2.medianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(image, 9, 300, 300)
        img = cv2.bitwise_and(color, color, mask=edges)

    # Status bar at bottom
    bar_color = (0, 100, 0) if detected else (60, 60, 60)
    cv2.rectangle(img, (0, h - 45), (w, h), bar_color, -1)
    cv2.putText(img, gesture_msg, (10, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if detected else (180, 180, 180), 2)
    return img

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real-Time Gesture & Filter Studio</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: 'Segoe UI', sans-serif; background: #121212; color: #e0e0e0; padding: 15px; }
            h1 { color: #4CAF50; text-align: center; margin-bottom: 12px; font-size: 1.4rem; }
            .controls { display: flex; flex-wrap: wrap; gap: 7px; justify-content: center; margin-bottom: 10px; }
            .btn { background: #4CAF50; color: white; border: none; padding: 8px 14px; border-radius: 5px; cursor: pointer; font-size: 13px; transition: 0.2s; }
            .btn:hover { background: #45a049; }
            .btn.active { background: #1b5e20; outline: 2px solid #81c784; }
            .btn-cam { background: #1565C0; }
            .btn-cam:hover { background: #0d47a1; }
            .btn-cam.on { background: #b71c1c; }
            .legend { text-align: center; font-size: 12px; color: #888; margin-bottom: 10px; }
            .video-area { display: flex; justify-content: center; }
            canvas { border-radius: 10px; border: 2px solid #333; max-width: 100%; }
            video { display: none; }
        </style>
    </head>
    <body>
        <h1>🎨 Real-Time Gesture & Filter Studio</h1>
        <div class="controls">
            <button id="camBtn" class="btn btn-cam" onclick="toggleCamera()">▶ Start Camera</button>
        </div>
        <div class="controls">
            <button onclick="setFilter(this,'original')" class="btn active">Original</button>
            <button onclick="setFilter(this,'red_tint')" class="btn">Red Tint</button>
            <button onclick="setFilter(this,'green_tint')" class="btn">Green Tint</button>
            <button onclick="setFilter(this,'blue_tint')" class="btn">Blue Tint</button>
            <button onclick="setFilter(this,'sepia')" class="btn">Sepia</button>
            <button onclick="setFilter(this,'cyan')" class="btn">Cyan</button>
            <button onclick="setFilter(this,'magenta')" class="btn">Magenta</button>
            <button onclick="setFilter(this,'sobel')" class="btn">Sobel</button>
            <button onclick="setFilter(this,'canny')" class="btn">Canny</button>
            <button onclick="setFilter(this,'cartoon')" class="btn">Cartoon</button>
        </div>
        <div class="legend">✋ Open Palm = Scroll Up &nbsp;|&nbsp; ✊ Fist = Scroll Down &nbsp;|&nbsp; Good lighting helps detection!</div>
        <div class="video-area">
            <video id="video" autoplay playsinline></video>
            <canvas id="output" width="640" height="480"></canvas>
        </div>
        <script>
            let currentFilter = 'original';
            let running = false;
            let stream = null;
            let processing = false;
            const video = document.getElementById('video');
            const canvas = document.getElementById('output');
            const ctx = canvas.getContext('2d');
            const camBtn = document.getElementById('camBtn');
            const offscreen = document.createElement('canvas');
            offscreen.width = 640; offscreen.height = 480;
            const offCtx = offscreen.getContext('2d');

            function setFilter(btn, ftype) {
                currentFilter = ftype;
                document.querySelectorAll('.btn:not(.btn-cam)').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }

            async function toggleCamera() {
                if (running) {
                    running = false;
                    if (stream) stream.getTracks().forEach(t => t.stop());
                    camBtn.textContent = '▶ Start Camera';
                    camBtn.classList.remove('on');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    return;
                }
                try {
                    stream = await navigator.mediaDevices.getUserMedia({
                        video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' }
                    });
                    video.srcObject = stream;
                    await video.play();
                    running = true;
                    camBtn.textContent = '⏹ Stop Camera';
                    camBtn.classList.add('on');
                    requestAnimationFrame(processLoop);
                } catch (e) {
                    alert('Camera error: ' + e.message);
                }
            }

            async function processLoop() {
                if (!running) return;
                if (!processing) {
                    processing = true;
                    offCtx.drawImage(video, 0, 0, 640, 480);
                    // Use high quality JPEG for better hand detection
                    const dataUrl = offscreen.toDataURL('image/jpeg', 0.95);
                    try {
                        const resp = await fetch('/frame', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ frame: dataUrl, ftype: currentFilter })
                        });
                        const data = await resp.json();
                        if (data.image) {
                            const img = new Image();
                            img.onload = () => {
                                ctx.drawImage(img, 0, 0);
                                processing = false;
                            };
                            img.src = 'data:image/jpeg;base64,' + data.image;
                        } else {
                            processing = false;
                        }
                    } catch(e) {
                        processing = false;
                    }
                }
                requestAnimationFrame(processLoop);
            }
        </script>
    </body>
    </html>
    """)

@app.route('/frame', methods=['POST'])
def frame():
    data = request.json
    header, encoded = data['frame'].split(',', 1)
    nparr = np.frombuffer(base64.b64decode(encoded), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return jsonify({'image': ''})
    img = cv2.flip(img, 1)
    processed = process_frame(img, data.get('ftype', 'original'))
    return jsonify({'image': image_to_base64(processed)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

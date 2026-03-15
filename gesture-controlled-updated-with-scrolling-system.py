## try asking a AI if it does not work 
import cv2
import numpy as np
from flask import Flask, render_template_string, request, jsonify
import base64
import os
import time

try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except (ImportError, AttributeError):
    HAS_MEDIAPIPE = False

app = Flask(__name__)

UPLOAD_FOLDER = 'real_time_color_filter_project/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MediaPipe Hands
if HAS_MEDIAPIPE:
    try:
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3
        )
        mp_draw = mp.solutions.drawing_utils
    except AttributeError:
        HAS_MEDIAPIPE = False

# Face Detection (OpenCV built-in)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# FPS tracking
frame_times = []

def image_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buffer).decode('utf-8')

def count_fingers(landmarks, handedness):
    tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    count = 0
    for tip in tips:
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
            count += 1
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    if (handedness == "Right" and thumb_tip.x > thumb_ip.x) or \
       (handedness == "Left" and thumb_tip.x < thumb_ip.x):
        count += 1
    return count

def get_gesture(count):
    gestures = {0: "✊ Fist", 1: "☝ One", 2: "✌ Two",
                3: "🤟 Three", 4: "🖖 Four", 5: "✋ Open Palm"}
    return gestures.get(count, f"{count} fingers")

def apply_filter(img, original, ftype):
    if ftype == "red_tint":
        img[:, :, 1] = img[:, :, 0] = 0
    elif ftype == "green_tint":
        img[:, :, 0] = img[:, :, 2] = 0
    elif ftype == "blue_tint":
        img[:, :, 1] = img[:, :, 2] = 0
    elif ftype == "sepia":
        s = cv2.transform(np.array(img, copy=True), np.matrix([
            [0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]))
        img = np.clip(s, 0, 255).astype(np.uint8)
    elif ftype == "cyan":
        img[:, :, 2] = 0
    elif ftype == "magenta":
        img[:, :, 1] = 0
    elif ftype == "sobel":
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        img = cv2.cvtColor(np.uint8(np.clip(cv2.magnitude(sx, sy), 0, 255)), cv2.COLOR_GRAY2BGR)
    elif ftype == "canny":
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(cv2.Canny(gray, 100, 200), cv2.COLOR_GRAY2BGR)
    elif ftype == "cartoon":
        gray = cv2.medianBlur(cv2.cvtColor(original, cv2.COLOR_BGR2GRAY), 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(original, 9, 300, 300)
        img = cv2.bitwise_and(color, color, mask=edges)
    elif ftype == "grayscale":
        img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    elif ftype == "invert":
        img = cv2.bitwise_not(img)
    elif ftype == "pixelate":
        h, w = img.shape[:2]
        small = cv2.resize(img, (w // 12, h // 12), interpolation=cv2.INTER_LINEAR)
        img = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    elif ftype == "warm":
        lut = np.arange(256, dtype=np.uint8)
        img[:, :, 2] = cv2.LUT(img[:, :, 2], np.clip(lut + 30, 0, 255).astype(np.uint8))
        img[:, :, 0] = cv2.LUT(img[:, :, 0], np.clip(lut - 20, 0, 255).astype(np.uint8))
    return img

def process_frame(image, ftype, show_face, show_landmarks):
    global frame_times
    img = image.copy()
    original = image.copy()
    h, w = img.shape[:2]
    gesture_msg = "No hand detected"
    detected = False
    total_fingers = 0

    # --- CLAHE contrast enhancement for detection ---
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
    proc = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)

    # --- Face Detection ---
    if show_face:
        gray_face = cv2.cvtColor(proc, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_face, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        for (fx, fy, fw, fh) in faces:
            cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), (0, 200, 255), 2)
            cv2.putText(img, "Face", (fx, fy - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)

    # --- Hand Detection ---
    if HAS_MEDIAPIPE:
        results = hands.process(cv2.cvtColor(proc, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks and results.multi_handedness:
            detected = True
            msgs = []
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                label = results.multi_handedness[i].classification[0].label
                if show_landmarks:
                    mp_draw.draw_landmarks(
                        img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                        mp_draw.DrawingSpec(color=(255, 80, 0), thickness=2)
                    )
                lm = hand_landmarks.landmark
                th = mp_hands.HandLandmark.THUMB_TIP
                ix = mp_hands.HandLandmark.INDEX_FINGER_TIP
                tp = (int(lm[th].x * w), int(lm[th].y * h))
                ip = (int(lm[ix].x * w), int(lm[ix].y * h))
                cv2.circle(img, tp, 8, (255, 80, 0), cv2.FILLED)
                cv2.circle(img, ip, 8, (255, 80, 0), cv2.FILLED)
                cv2.line(img, tp, ip, (0, 255, 255), 2)
                count = count_fingers(hand_landmarks, label)
                total_fingers += count
                gesture = get_gesture(count)
                msgs.append(f"{label}: {gesture}")
            gesture_msg = "  |  ".join(msgs)

            # Big finger count display
            cv2.putText(img, str(total_fingers), (w - 70, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 5)

    # --- Apply filter ---
    img = apply_filter(img, original, ftype)

    # --- FPS ---
    now = time.time()
    frame_times.append(now)
    frame_times = [t for t in frame_times if now - t < 1.0]
    fps = len(frame_times)

    # --- Top HUD ---
    cv2.rectangle(img, (0, 0), (w, 38), (0, 0, 0), -1)
    cv2.putText(img, f"FPS: {fps}", (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)
    cv2.putText(img, f"Filter: {ftype.replace('_', ' ').title()}", (90, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

    # --- Bottom Status Bar ---
    bar_color = (0, 90, 0) if detected else (40, 40, 40)
    cv2.rectangle(img, (0, h - 42), (w, h), bar_color, -1)
    txt_color = (0, 255, 100) if detected else (160, 160, 160)
    cv2.putText(img, gesture_msg, (10, h - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.65, txt_color, 2)

    return img

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real-Time Gesture Studio</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: 'Segoe UI', sans-serif; background: #0d0d0d; color: #e0e0e0; padding: 12px; }
            h1 { color: #4CAF50; text-align: center; margin-bottom: 10px; font-size: 1.3rem; }
            .row { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin-bottom: 8px; }
            .btn { background: #2e7d32; color: white; border: none; padding: 7px 13px; border-radius: 5px; cursor: pointer; font-size: 12px; transition: 0.2s; }
            .btn:hover { opacity: 0.85; }
            .btn.active { outline: 2px solid #81c784; background: #1b5e20; }
            .btn-blue { background: #1565C0; }
            .btn-blue.on { background: #b71c1c; }
            .btn-orange { background: #e65100; }
            .btn-purple { background: #6a1b9a; }
            .btn-teal { background: #00695c; }
            .toggle-group { display: flex; gap: 6px; align-items: center; }
            .toggle { background: #333; color: #aaa; border: 1px solid #555; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-size: 12px; }
            .toggle.on { background: #4CAF50; color: white; border-color: #4CAF50; }
            .legend { text-align: center; font-size: 11px; color: #666; margin-bottom: 8px; }
            .video-wrap { display: flex; justify-content: center; }
            canvas { border-radius: 10px; border: 2px solid #2a2a2a; max-width: 100%; }
            video { display: none; }
        </style>
    </head>
    <body>
        <h1>🎨 Real-Time Gesture & Filter Studio</h1>

        <!-- Camera & Utility Controls -->
        <div class="row">
            <button id="camBtn" class="btn btn-blue" onclick="toggleCamera()">▶ Start Camera</button>
            <button class="btn btn-orange" onclick="takeSnapshot()">📸 Snapshot</button>
            <button id="mirrorBtn" class="toggle on" onclick="toggleMirror()">🔄 Mirror: ON</button>
            <button id="faceBtn" class="toggle on" onclick="toggleFace()">👤 Face Detect: ON</button>
            <button id="landmarkBtn" class="toggle on" onclick="toggleLandmarks()">🖐 Landmarks: ON</button>
        </div>

        <!-- Color Filters -->
        <div class="row">
            <b style="color:#888;font-size:12px;align-self:center;">Filters:</b>
            <button onclick="setFilter(this,'original')" class="btn active">Original</button>
            <button onclick="setFilter(this,'grayscale')" class="btn">Grayscale</button>
            <button onclick="setFilter(this,'invert')" class="btn">Invert</button>
            <button onclick="setFilter(this,'warm')" class="btn btn-orange">Warm</button>
            <button onclick="setFilter(this,'sepia')" class="btn btn-orange">Sepia</button>
            <button onclick="setFilter(this,'pixelate')" class="btn btn-purple">Pixelate</button>
            <button onclick="setFilter(this,'red_tint')" class="btn" style="background:#c62828">Red</button>
            <button onclick="setFilter(this,'green_tint')" class="btn">Green</button>
            <button onclick="setFilter(this,'blue_tint')" class="btn btn-blue">Blue</button>
            <button onclick="setFilter(this,'cyan')" class="btn btn-teal">Cyan</button>
            <button onclick="setFilter(this,'magenta')" class="btn btn-purple">Magenta</button>
            <button onclick="setFilter(this,'sobel')" class="btn" style="background:#37474f">Sobel</button>
            <button onclick="setFilter(this,'canny')" class="btn" style="background:#37474f">Canny</button>
            <button onclick="setFilter(this,'cartoon')" class="btn" style="background:#4a148c">Cartoon</button>
        </div>

        <div class="legend">✋ Open Palm = 5 fingers &nbsp;|&nbsp; ✊ Fist = 0 &nbsp;|&nbsp; Number shown top-right = finger count</div>

        <div class="video-wrap">
            <video id="video" autoplay playsinline></video>
            <canvas id="output" width="640" height="480"></canvas>
        </div>

        <script>
            let currentFilter = 'original';
            let running = false, processing = false;
            let stream = null;
            let mirrorOn = true, faceOn = true, landmarksOn = true;

            const video = document.getElementById('video');
            const canvas = document.getElementById('output');
            const ctx = canvas.getContext('2d');
            const camBtn = document.getElementById('camBtn');
            const offscreen = document.createElement('canvas');
            offscreen.width = 640; offscreen.height = 480;
            const offCtx = offscreen.getContext('2d');

            function setFilter(btn, ftype) {
                currentFilter = ftype;
                document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }

            function toggleMirror() {
                mirrorOn = !mirrorOn;
                const btn = document.getElementById('mirrorBtn');
                btn.textContent = mirrorOn ? '🔄 Mirror: ON' : '🔄 Mirror: OFF';
                btn.classList.toggle('on', mirrorOn);
            }

            function toggleFace() {
                faceOn = !faceOn;
                const btn = document.getElementById('faceBtn');
                btn.textContent = faceOn ? '👤 Face Detect: ON' : '👤 Face Detect: OFF';
                btn.classList.toggle('on', faceOn);
            }

            function toggleLandmarks() {
                landmarksOn = !landmarksOn;
                const btn = document.getElementById('landmarkBtn');
                btn.textContent = landmarksOn ? '🖐 Landmarks: ON' : '🖐 Landmarks: OFF';
                btn.classList.toggle('on', landmarksOn);
            }

            function takeSnapshot() {
                const link = document.createElement('a');
                link.href = canvas.toDataURL('image/jpeg', 0.95);
                link.download = 'snapshot_' + Date.now() + '.jpg';
                link.click();
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
                    if (mirrorOn) {
                        offCtx.save();
                        offCtx.translate(640, 0);
                        offCtx.scale(-1, 1);
                        offCtx.drawImage(video, 0, 0, 640, 480);
                        offCtx.restore();
                    } else {
                        offCtx.drawImage(video, 0, 0, 640, 480);
                    }
                    const dataUrl = offscreen.toDataURL('image/jpeg', 0.95);
                    try {
                        const resp = await fetch('/frame', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                frame: dataUrl,
                                ftype: currentFilter,
                                show_face: faceOn,
                                show_landmarks: landmarksOn
                            })
                        });
                        const data = await resp.json();
                        if (data.image) {
                            const img = new Image();
                            img.onload = () => { ctx.drawImage(img, 0, 0); processing = false; };
                            img.src = 'data:image/jpeg;base64,' + data.image;
                        } else { processing = false; }
                    } catch(e) { processing = false; }
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
    processed = process_frame(
        img,
        data.get('ftype', 'original'),
        data.get('show_face', True),
        data.get('show_landmarks', True)
    )
    return jsonify({'image': image_to_base64(processed)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

import cv2
import mediapipe as mp
import numpy as np
import math
import screen_brightness_control as sbc   # for brightness
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Initialize audio control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = IAudioEndpointVolume(interface)

# Get volume range
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

# Webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            lm = hand_landmarks.landmark

            # Thumb tip and index tip
            thumb_tip = (int(lm[mp_hands.HandLandmark.THUMB_TIP].x * w),
                         int(lm[mp_hands.HandLandmark.THUMB_TIP].y * h))
            index_tip = (int(lm[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w),
                         int(lm[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h))

            # Draw points
            cv2.circle(img, thumb_tip, 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, index_tip, 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, thumb_tip, index_tip, (255, 0, 0), 2)

            # Distance
            dist = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])

            # Map distance to volume (0–100%)
            vol = np.interp(dist, [20, 200], [min_vol, max_vol])
            volume.SetMasterVolumeLevel(vol, None)

            # Map distance to brightness (0–100%)
            bright = np.interp(dist, [20, 200], [0, 100])
            sbc.set_brightness(int(bright))

            cv2.putText(img, f"Vol:{int(np.interp(vol, [min_vol, max_vol], [0,100]))}% Bright:{int(bright)}%",
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()

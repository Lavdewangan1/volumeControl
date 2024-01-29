import cv2
import mediapipe as mp
import time
from math import hypot, atan2, degrees
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import keyboard
import pyautogui

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]

# Initialize state variables
catching_state = False
playpause_state = False

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id, lm in enumerate(handlandmark.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

    if lmList != []:
        x1, y1 = lmList[4][1], lmList[4][2]  # thumb
        x_pinky, y_pinky = lmList[20][1], lmList[20][2]  # pinky
        x_index, y_index = lmList[8][1], lmList[8][2]  # index

        # Calculate distances
        distance_thumb_pinky = hypot(x_pinky - x1, y_pinky - y1)
        distance_thumb_index = hypot(x_index - x1, y_index - y1)

        print(distance_thumb_pinky, distance_thumb_index)

        # Toggle catching state
        if distance_thumb_pinky < 30 and distance_thumb_index < 30:
            catching_state = not catching_state
            time.sleep(1.5)
            if catching_state:
                print("\n Catching for volume change...")

        # Toggle play/pause state
        if (
            distance_thumb_pinky < 30
            and distance_thumb_index < 30
            and not catching_state
        ):
            playpause_state = not playpause_state
            time.sleep(1.5)
            if playpause_state:
                print("Play/Pause")

        # Volume change logic
        if catching_state and distance_thumb_index > 70:
            angle = -degrees(atan2(y_index - y1, x_index - x1))
            vol = np.interp(angle, [30, 150], [volMin, volMax])
            volbar = np.interp(angle, [30, 150], [400, 150])
            cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 4)
            cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 0, 255), cv2.FILLED)

            if angle < 90:
                keyboard.press_and_release("volume down")
            else:
                keyboard.press_and_release("volume up")

    # Play/Pause logic
    if playpause_state and distance_thumb_index < 30:
        pyautogui.keyDown("playpause")
        pyautogui.keyUp("playpause")


cap.release()
cv2.destroyAllWindows()

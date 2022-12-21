import cv2
import mediapipe as mp
import time
from track import TrackData, TrackingAlgo
from led import led_thread, DisplayAlgo
from comms import Message

# Message.playback()

# Message.clear_save()
# led_thread.start()
# led_thread.join()
# exit()

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


flag = reset = False
track_data0 = None

while True:
    success, img = cap.read()
    frame_width  = cap.get(3) # 1080.0 1920.0 y,x
    frame_height = cap.get(4)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            track_data = TrackData.from_handLms(handLms, img)

            if flag:
                if reset:
                    track_data0 = track_data
                    reset = False
                
                TrackingAlgo.hand_finger_control(track_data0, track_data)
            
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    
    cv2.imshow('frame', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        led_thread.start()
        flag = True
        reset = True
    if key == ord("q"):
        DisplayAlgo.STOP_FLAG = True
        exit(0)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

led_thread.join()
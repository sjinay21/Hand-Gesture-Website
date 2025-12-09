# import cv2
# from cvzone.HandTrackingModule import HandDetector
# from pynput.keyboard import Controller
# import cvzone
# import time

# # Initialize webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)

# # Ensure camera is opened correctly
# if not cap.isOpened():
#     print("❌ ERROR: Camera not detected. Check your webcam connection.")
#     exit()

# detector = HandDetector(detectionCon=0.8, maxHands=1)
# keyboard = Controller()
# keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
#         ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
#         ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# finalText = ""
# buttonList = []

# class Button:
#     def __init__(self, pos, text, size=(85, 85)):
#         self.pos = pos
#         self.size = size
#         self.text = text
#         self.last_pressed = 0  # Prevent multiple key presses

# # Create buttons
# for i in range(len(keys)):
#     for j, key in enumerate(keys[i]):
#         buttonList.append(Button((100 * j + 50, 100 * i + 50), key))

# def drawAll(img, buttonList):
#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
#         cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
#         cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
#         cv2.putText(img, button.text, (x + 20, y + 65),
#                     cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
#     return img

# while True:
#     success, img = cap.read()
#     if not success or img is None:
#         print("❌ ERROR: Failed to capture image from webcam. Retrying...")
#         continue

#     hands, img = detector.findHands(img)  # Detect hands
#     img = drawAll(img, buttonList)

#     if hands:
#         lmList = hands[0]['lmList']  # Extract hand landmarks

#         for button in buttonList:
#             x, y = button.pos
#             w, h = button.size

#             # Check if index finger is inside the button
#             if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
#                 cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
#                 cv2.putText(img, button.text, (x + 20, y + 65),
#                             cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

#                 # Ensure landmarks exist before finding distance
#                 if len(lmList) > 12:
#                     try:
#                         distance_info = detector.findDistance(lmList[8], lmList[12])

#                         # Ensure we received valid output (it should be a tuple)
#                         if isinstance(distance_info, tuple) and len(distance_info) == 3:
#                             l, _, _ = distance_info

#                             # If fingers are close together, register as a key press
#                             if l < 30 and time.time() - button.last_pressed > 0.3:  # Avoid multiple presses
#                                 keyboard.press(button.text.lower())
#                                 finalText += button.text
#                                 button.last_pressed = time.time()

#                                 cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
#                                 cv2.putText(img, button.text, (x + 20, y + 65),
#                                             cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
#                         else:
#                             print("⚠️ ERROR: findDistance() returned unexpected data:", distance_info)
#                     except Exception as e:
#                         print("⚠️ ERROR in findDistance():", e)

#     # Display typed text
#     cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
#     cv2.putText(img, finalText, (60, 430),
#                 cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

#     cv2.imshow("Virtual Keyboard", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()







import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
import cvzone
import time
import pyautogui  # Simulate global keypress

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

if not cap.isOpened():
    print("❌ ERROR: Camera not detected. Check your webcam connection.")
    exit()

# Hand detection
detector = HandDetector(detectionCon=0.8, maxHands=1)
keyboard = Controller()
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["Space"]]
        # ["Ctrl", "Alt", "Shift", "Enter"]]

buttonList = []

class Button:
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos
        self.size = size
        self.text = text
        self.last_pressed = 0  # Avoid multiple presses

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        w, h = (300, 85) if key == "Space" else (85, 85)
        buttonList.append(Button((100 * j + 50, 100 * i + 50), key, (w, h)))

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

while True:
    success, img = cap.read()
    if not success or img is None:
        print("❌ ERROR: Failed to capture image from webcam. Retrying...")
        continue

    hands, img = detector.findHands(img)
    img = drawAll(img, buttonList)

    if hands:
        lmList = hands[0]['lmList']

        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                # Ensure landmarks exist before finding distance
                if len(lmList) > 12:
                    try:
                        distance_info = detector.findDistance(lmList[8][:2], lmList[12][:2])  # Only take (x, y)

                        if isinstance(distance_info, tuple) and len(distance_info) >= 2:
                            l = distance_info[0]  # Extract distance

                            if l < 30 and time.time() - button.last_pressed > 0.3:
                                pyautogui.write(" " if button.text == "Space" else button.text.lower())
                                button.last_pressed = time.time()

                                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                                cv2.putText(img, button.text, (x + 20, y + 65),
                                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        else:
                            print("⚠️ ERROR: findDistance() returned unexpected data:", distance_info)
                    except Exception as e:
                        print("⚠️ ERROR in findDistance():", e)

    # Mouse Click Detection
    mouse_x, mouse_y = pyautogui.position()
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        if x < mouse_x < x + w and y < mouse_y < y + h:
            if pyautogui.mouseDown():
                pyautogui.write(" " if button.text == "Space" else button.text.lower())

    cv2.imshow("AI Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

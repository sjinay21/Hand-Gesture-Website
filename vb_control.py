# import cv2
# import numpy as np
# import mediapipe as mp
# import screen_brightness_control as sbc
# from math import hypot
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL

# def main():
#     # Initialize audio controls
#     try:
#         devices = AudioUtilities.GetSpeakers()
#         interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#         volume = cast(interface, POINTER(IAudioEndpointVolume))
#         volRange = volume.GetVolumeRange()
#         minVol, maxVol = volRange[0], volRange[1]
#     except Exception as e:
#         print(f"Error initializing audio: {e}")
#         return

#     # Initialize MediaPipe
#     mp_hands = mp.solutions.hands
#     hands = mp_hands.Hands(
#         static_image_mode=False,
#         max_num_hands=2,
#         min_detection_confidence=0.7,
#         min_tracking_confidence=0.7
#     )
#     mp_draw = mp.solutions.drawing_utils

#     # Initialize camera
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not open camera")
#         return

#     try:
#         while True:
#             success, img = cap.read()
#             if not success:
#                 print("Error: Failed to grab frame")
#                 break

#             # Flip the image horizontally for a later selfie-view display
#             img = cv2.flip(img, 1)
            
#             # Convert BGR to RGB
#             imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
#             # Process the image and detect hands
#             results = hands.process(imgRGB)

#             left_hand_landmarks = []
#             right_hand_landmarks = []

#             if results.multi_hand_landmarks and results.multi_handedness:
#                 for idx, hand_handedness in enumerate(results.multi_handedness):
#                     hand_label = hand_handedness.classification[0].label
#                     hand_landmarks = results.multi_hand_landmarks[idx]

#                     # Draw landmarks
#                     mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#                     # Get thumb and index finger landmarks
#                     landmarks = []
#                     for id in [4, 8]:  # 4 is thumb tip, 8 is index finger tip
#                         cx = int(hand_landmarks.landmark[id].x * img.shape[1])
#                         cy = int(hand_landmarks.landmark[id].y * img.shape[0])
#                         landmarks.append([cx, cy])

#                     if hand_label == "Left":
#                         left_hand_landmarks = landmarks
#                     else:
#                         right_hand_landmarks = landmarks

#                     # Draw circles on thumb and index tips
#                     if landmarks:
#                         cv2.circle(img, (landmarks[0][0], landmarks[0][1]), 10, (255, 0, 0), cv2.FILLED)
#                         cv2.circle(img, (landmarks[1][0], landmarks[1][1]), 10, (255, 0, 0), cv2.FILLED)
#                         cv2.line(img, (landmarks[0][0], landmarks[0][1]), 
#                                 (landmarks[1][0], landmarks[1][1]), (255, 0, 0), 3)

#             # Process left hand for brightness
#             if left_hand_landmarks:
#                 length = hypot(left_hand_landmarks[1][0] - left_hand_landmarks[0][0],
#                              left_hand_landmarks[1][1] - left_hand_landmarks[0][1])
                
#                 # Convert length to brightness (50-300 -> 0-100)
#                 brightness = np.interp(length, [50, 300], [0, 100])
#                 brightness = int(brightness)
                
#                 try:
#                     sbc.set_brightness(brightness)
#                     # Display brightness level
#                     cv2.putText(img, f'Brightness: {brightness}%', (10, 50), 
#                               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#                 except Exception as e:
#                     print(f"Error setting brightness: {e}")

#             # Process right hand for volume
#             if right_hand_landmarks:
#                 length = hypot(right_hand_landmarks[1][0] - right_hand_landmarks[0][0],
#                              right_hand_landmarks[1][1] - right_hand_landmarks[0][1])
                
#                 # Convert length to volume (50-300 -> min_vol-max_vol)
#                 vol = np.interp(length, [50, 300], [minVol, maxVol])
                
#                 try:
#                     volume.SetMasterVolumeLevel(vol, None)
#                     # Convert volume to percentage for display
#                     vol_percentage = int(np.interp(vol, [minVol, maxVol], [0, 100]))
#                     cv2.putText(img, f'Volume: {vol_percentage}%', (10, 100), 
#                               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#                 except Exception as e:
#                     print(f"Error setting volume: {e}")

#             # Display the image
#             cv2.imshow('Hand Gesture Control', img)

#             # Break loop with 'q'
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#     finally:
#         # Clean up
#         cap.release()
#         cv2.destroyAllWindows()
#         hands.close()

# if __name__ == "__main__":
#     main()


import cv2
import mediapipe as mp
import numpy as np
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import pyautogui
import win32gui
import win32con
import time
from datetime import datetime
import os

class GestureController:
    def __init__(self):
        # Initialize MediaPipe Hand detection
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Initialize volume control
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.volRange = self.volume.GetVolumeRange()
        self.minVol, self.maxVol = self.volRange[0], self.volRange[1]

        # Initialize video capture
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Control bar parameters
        self.bar_start_x = 50
        self.bar_width = 200
        self.bar_height = 30
        self.brightness_y = 50
        self.volume_y = 100

        # Gesture states
        self.mouse_mode = False
        self.last_gesture = None
        self.gesture_start_time = 0
        self.screenshot_cooldown = 0
        
        # Create screenshots directory if it doesn't exist
        self.screenshot_dir = "screenshots"
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    def draw_control_bar(self, img, value, y_position, color, label):
        # Draw background bar
        cv2.rectangle(img, 
                     (self.bar_start_x, y_position), 
                     (self.bar_start_x + self.bar_width, y_position + self.bar_height), 
                     (50, 50, 50), 
                     cv2.FILLED)
        
        # Draw value bar
        filled_width = int((value / 100) * self.bar_width)
        cv2.rectangle(img, 
                     (self.bar_start_x, y_position), 
                     (self.bar_start_x + filled_width, y_position + self.bar_height), 
                     color, 
                     cv2.FILLED)
        
        # Draw border
        cv2.rectangle(img, 
                     (self.bar_start_x, y_position), 
                     (self.bar_start_x + self.bar_width, y_position + self.bar_height), 
                     (255, 255, 255), 
                     2)
        
        # Add label and value
        cv2.putText(img, 
                    f"{label}: {int(value)}%", 
                    (self.bar_start_x + self.bar_width + 10, y_position + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, 
                    (255, 255, 255), 
                    2)

    def draw_mode_indicator(self, img, text, position, color=(255, 255, 255)):
        cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    def get_hand_gesture(self, landmarks):
        # Get relevant finger landmarks
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]
        
        # Calculate distances
        thumb_index_dist = hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
        index_middle_dist = hypot(index_tip.x - middle_tip.x, index_tip.y - middle_tip.y)
        
        # Detect gestures
        if thumb_index_dist < 0.05:  # Thumb and index touching
            return "CLICK"
        elif index_middle_dist < 0.05:  # Index and middle touching
            return "DOUBLE_CLICK"
        elif all(l.y < thumb_tip.y for l in [index_tip, middle_tip, ring_tip, pinky_tip]):  # All fingers up
            return "MOUSE_MODE"
        
        return None

    def take_screenshot(self):
        if time.time() - self.screenshot_cooldown > 2:  # 2 second cooldown
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.screenshot_dir}/screenshot_{timestamp}.png"
            pyautogui.screenshot(filename)
            print(f"Screenshot saved: {filename}")
            self.screenshot_cooldown = time.time()

    def minimize_window(self):
        window = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(window, win32con.SW_MINIMIZE)

    def process_hands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Get hand gesture
                gesture = self.get_hand_gesture(hand_landmarks)
                
                # Process gestures
                if gesture:
                    if gesture != self.last_gesture:
                        self.last_gesture = gesture
                        self.gesture_start_time = time.time()
                    
                    # Mouse control mode
                    if gesture == "MOUSE_MODE":
                        self.mouse_mode = True
                        index_tip = hand_landmarks.landmark[8]
                        mouse_x = int(index_tip.x * self.screen_width)
                        mouse_y = int(index_tip.y * self.screen_height)
                        pyautogui.moveTo(mouse_x, mouse_y, duration=0.1)
                    
                    # Click actions
                    elif gesture == "CLICK" and time.time() - self.gesture_start_time > 0.3:
                        pyautogui.click()
                        time.sleep(0.3)
                    elif gesture == "DOUBLE_CLICK" and time.time() - self.gesture_start_time > 0.3:
                        pyautogui.doubleClick()
                        time.sleep(0.3)
                else:
                    self.mouse_mode = False
                    self.last_gesture = None

                # Process volume and brightness
                if hand_idx == 0:  # First hand
                    thumb_tip = (int(hand_landmarks.landmark[4].x * img.shape[1]),
                               int(hand_landmarks.landmark[4].y * img.shape[0]))
                    index_tip = (int(hand_landmarks.landmark[8].x * img.shape[1]),
                               int(hand_landmarks.landmark[8].y * img.shape[0]))
                    
                    length = hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])
                    vol = np.interp(length, [50, 250], [self.minVol, self.maxVol])
                    try:
                        self.volume.SetMasterVolumeLevel(vol, None)
                        vol_percentage = int(np.interp(vol, [self.minVol, self.maxVol], [0, 100]))
                        self.draw_control_bar(img, vol_percentage, self.volume_y, (0, 0, 255), "Volume")
                    except Exception as e:
                        print(f"Error setting volume: {e}")

                elif hand_idx == 1:  # Second hand
                    thumb_tip = (int(hand_landmarks.landmark[4].x * img.shape[1]),
                               int(hand_landmarks.landmark[4].y * img.shape[0]))
                    index_tip = (int(hand_landmarks.landmark[8].x * img.shape[1]),
                               int(hand_landmarks.landmark[8].y * img.shape[0]))
                    
                    length = hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])
                    brightness = int(np.interp(length, [50, 250], [0, 100]))
                    try:
                        sbc.set_brightness(brightness)
                        self.draw_control_bar(img, brightness, self.brightness_y, (0, 255, 0), "Brightness")
                    except Exception as e:
                        print(f"Error setting brightness: {e}")

        return img

    def run(self):
        try:
            while True:
                success, img = self.cap.read()
                if not success:
                    print("Failed to get frame from camera")
                    break

                img = cv2.flip(img, 1)
                img = self.process_hands(img)

                # Draw mode indicators
                self.draw_mode_indicator(img, "Mouse Mode: " + ("ON" if self.mouse_mode else "OFF"), (10, 30))
                
                # Display help text
                help_text = [
                    "Controls:",
                    "- Raise all fingers: Mouse control",
                    "- Thumb + Index touch: Click",
                    "- Index + Middle touch: Double click",
                    "- Hand 1: Volume control",
                    "- Hand 2: Brightness control",
                    "Press 'q' to quit, 's' for screenshot, 'm' to minimize"
                ]
                
                for i, text in enumerate(help_text):
                    cv2.putText(img, text, (10, 400 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                cv2.imshow('Gesture Control', img)

                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    self.take_screenshot()
                elif key == ord('m'):
                    self.minimize_window()

        finally:
            self.cap.release()
            cv2.destroyAllWindows()
            self.hands.close()

def main():
    controller = GestureController()
    controller.run()

if __name__ == "__main__":
    main()
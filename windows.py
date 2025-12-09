# import cv2
# import mediapipe as mp
# import os
# import time
# from typing import Dict

# class GestureAppLauncher:
#     def __init__(self):
#         # Initialize MediaPipe Hand detection
#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands(
#             static_image_mode=False,
#             max_num_hands=1,
#             min_detection_confidence=0.7,
#             min_tracking_confidence=0.7
#         )
#         self.mp_draw = mp.solutions.drawing_utils
        
#         # Dictionary mapping gestures to applications
#         self.gesture_apps = {
#             "open_palm": ("Notepad", "notepad.exe"),
#             "fist": ("Calculator", "calc.exe"),
#             "thumbs_up": ("Paint", "mspaint.exe"),
#             "peace": ("Command Prompt", "cmd.exe"),
#             "three_fingers": ("File Explorer", "explorer.exe"),
#         }
        
#         self.last_launch_time = 0
#         self.cooldown = 2

#     def launch_app(self, gesture: str) -> None:
#         current_time = time.time()
#         if current_time - self.last_launch_time < self.cooldown:
#             return
        
#         if gesture in self.gesture_apps:
#             app_name, app_command = self.gesture_apps[gesture]
#             try:
#                 os.system(f"start {app_command}")
#                 print(f"Launching {app_name}")
#                 self.last_launch_time = current_time
#             except Exception as e:
#                 print(f"Error launching {app_name}: {str(e)}")

#     def start(self):
#         # Initialize the camera
#         cap = cv2.VideoCapture(0)
        
#         # Check if camera opened successfully
#         if not cap.isOpened():
#             print("Error: Could not open camera")
#             return

#         # Set camera properties
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#         print("Camera initialized successfully!")
#         print("Press 'q' to quit")

#         while True:
#             # Read frame from camera
#             ret, frame = cap.read()
#             if not ret:
#                 print("Failed to grab frame")
#                 break

#             # Flip the frame horizontally for a later selfie-view display
#             frame = cv2.flip(frame, 1)
            
#             # Convert BGR to RGB
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
#             # Process the frame and detect hands
#             results = self.hands.process(rgb_frame)

#             # Draw hand landmarks
#             if results.multi_hand_landmarks:
#                 for hand_landmarks in results.multi_hand_landmarks:
#                     self.mp_draw.draw_landmarks(
#                         frame,
#                         hand_landmarks,
#                         self.mp_hands.HAND_CONNECTIONS
#                     )

#                     # Get hand gesture and launch corresponding app
#                     # You can add your gesture recognition logic here
#                     # For now, it will just detect if a hand is present
#                     self.launch_app("open_palm")  # Example: launches notepad when hand is detected

#             # Display the frame
#             cv2.imshow('Gesture Control', frame)

#             # Break the loop if 'q' is pressed
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         # Release the camera and close windows
#         cap.release()
#         cv2.destroyAllWindows()

# if __name__ == "__main__":
#     launcher = GestureAppLauncher()
#     launcher.start()






import cv2
import mediapipe as mp
import os
import time
import numpy as np
from typing import Dict, Tuple

class GestureAppLauncher:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Dictionary mapping gestures to applications with descriptions
        self.gesture_apps = {
            "Open Palm": ("Notepad", "notepad.exe"),
            "Fist": ("Calculator", "calc.exe"),
            "Thumbs Up": ("Paint", "mspaint.exe"),
            "Peace": ("Command Prompt", "cmd.exe"),
            "Three Fingers": ("File Explorer", "explorer.exe"),
        }
        
        self.last_launch_time = 0
        self.cooldown = 2
        self.current_gesture = None

    def detect_gesture(self, hand_landmarks) -> str:
        # Get landmark coordinates
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.append([lm.x, lm.y, lm.z])
        
        # Calculate finger states (extended or not)
        thumb_extended = landmarks[4][0] > landmarks[3][0]  # For right hand
        index_extended = landmarks[8][1] < landmarks[6][1]
        middle_extended = landmarks[12][1] < landmarks[10][1]
        ring_extended = landmarks[16][1] < landmarks[14][1]
        pinky_extended = landmarks[20][1] < landmarks[18][1]
        
        # Detect gestures based on finger states
        if all([index_extended, middle_extended, ring_extended, pinky_extended]) and not thumb_extended:
            return "Open Palm"
        elif not any([thumb_extended, index_extended, middle_extended, ring_extended, pinky_extended]):
            return "Fist"
        elif thumb_extended and not any([index_extended, middle_extended, ring_extended, pinky_extended]):
            return "Thumbs Up"
        elif index_extended and middle_extended and not any([thumb_extended, ring_extended, pinky_extended]):
            return "Peace"
        elif index_extended and middle_extended and ring_extended and not any([thumb_extended, pinky_extended]):
            return "Three Fingers"
        
        return None

    def draw_command_panel(self, frame):
        overlay = frame.copy()
        panel_width = 300
        
        cv2.rectangle(overlay, (frame.shape[1] - panel_width, 0), 
                     (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)

        cv2.putText(frame, "Available Commands", 
                   (frame.shape[1] - panel_width + 10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv2.line(frame, 
                 (frame.shape[1] - panel_width + 10, 40),
                 (frame.shape[1] - 10, 40),
                 (255, 255, 255), 1)

        y_offset = 80
        for gesture, (app_name, _) in self.gesture_apps.items():
            # Highlight current gesture
            color = (0, 255, 0) if gesture == self.current_gesture else (255, 255, 255)
            
            cv2.putText(frame, gesture,
                       (frame.shape[1] - panel_width + 10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
            
            cv2.putText(frame, f"→ {app_name}",
                       (frame.shape[1] - panel_width + 30, y_offset + 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            y_offset += 60

        controls_y = y_offset + 20
        cv2.putText(frame, "Controls:", 
                   (frame.shape[1] - panel_width + 10, controls_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        controls = [
            "Press 'q' to quit",
            "Press 'r' to reset",
            "Press 'h' to hide/show panel"
        ]
        
        for i, control in enumerate(controls):
            cv2.putText(frame, control,
                       (frame.shape[1] - panel_width + 10, controls_y + 30 + (i * 25)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        return frame

    def launch_app(self, gesture: str) -> None:
        current_time = time.time()
        if current_time - self.last_launch_time < self.cooldown:
            return
        
        if gesture in self.gesture_apps:
            app_name, app_command = self.gesture_apps[gesture]
            try:
                os.system(f"start {app_command}")
                print(f"Launching {app_name}")
                self.last_launch_time = current_time
            except Exception as e:
                print(f"Error launching {app_name}: {str(e)}")

    def start(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        print("Camera initialized successfully!")
        print("Press 'q' to quit")

        show_panel = True

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            self.current_gesture = None  # Reset current gesture

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        self.mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2)
                    )

                    # Detect and process gesture
                    self.current_gesture = self.detect_gesture(hand_landmarks)
                    if self.current_gesture:
                        self.launch_app(self.current_gesture)

            # Draw FPS
            fps = cap.get(cv2.CAP_PROP_FPS)
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Draw current gesture
            if self.current_gesture:
                cv2.putText(frame, f"Gesture: {self.current_gesture}", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if show_panel:
                frame = self.draw_command_panel(frame)

            cv2.imshow('Gesture Control', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('h'):
                show_panel = not show_panel
            elif key == ord('r'):
                self.last_launch_time = 0

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    launcher = GestureAppLauncher()
    launcher.start()

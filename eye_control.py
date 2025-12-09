import cv2
import pyautogui
import numpy as np
import mediapipe as mp
import time
import keyboard

# Initialize Mediapipe Face Meshe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Get screen dimensionse
screen_width, screen_height = pyautogui.size()

# Exponential smoothing factor for mouse movement
SMOOTHING_FACTOR = 0.8
previous_x, previous_y = 0, 0

# Flags for advanced functionalities
eye_control_enabled = True
blink_detected = False
dwell_start_time = None
dwell_duration = 1.5  # Seconds to trigger dwell click

# Mediapipe landmarks for eyes
LEFT_EYE_INDICES = [33, 133, 159, 145, 160, 144]  # Points around the left eye
RIGHT_EYE_INDICES = [362, 263, 387, 373, 386, 374]  # Points around the right eye
EYE_BLINK_THRESHOLD = 0.2  # Aspect ratio threshold to detect a blink

# Function to map eye position to screen coordinates
def map_to_screen(x, y, frame_width, frame_height):
    screen_x = np.interp(x, [0, frame_width], [0, screen_width])
    screen_y = np.interp(y, [0, frame_height], [0, screen_height])
    return int(screen_x), int(screen_y)

# Function to calculate eye aspect ratio (EAR) for blink detection
def calculate_eye_aspect_ratio(landmarks, eye_indices, frame_width, frame_height):
    points = [(landmarks[i][0] * frame_width, landmarks[i][1] * frame_height) for i in eye_indices]
    vertical_1 = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
    vertical_2 = np.linalg.norm(np.array(points[2]) - np.array(points[4]))
    horizontal = np.linalg.norm(np.array(points[0]) - np.array(points[3]))
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear

# Video capture
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with Mediapipe
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extract landmarks
                landmarks = [(lm.x, lm.y) for lm in face_landmarks.landmark]
                # Calculate eye centers
                left_eye_center_x = np.mean([landmarks[i][0] for i in LEFT_EYE_INDICES]) * frame_width
                left_eye_center_y = np.mean([landmarks[i][1] for i in LEFT_EYE_INDICES]) * frame_height
                right_eye_center_x = np.mean([landmarks[i][0] for i in RIGHT_EYE_INDICES]) * frame_width
                right_eye_center_y = np.mean([landmarks[i][1] for i in RIGHT_EYE_INDICES]) * frame_height

                # Calculate average eye center
                avg_eye_x = (left_eye_center_x + right_eye_center_x) // 2
                avg_eye_y = (left_eye_center_y + right_eye_center_y) // 2

                # Eye aspect ratio (EAR) for blink detection
                left_ear = calculate_eye_aspect_ratio(landmarks, LEFT_EYE_INDICES, frame_width, frame_height)
                right_ear = calculate_eye_aspect_ratio(landmarks, RIGHT_EYE_INDICES, frame_width, frame_height)

                # Detect blink based on EAR threshold
                if left_ear < EYE_BLINK_THRESHOLD and right_ear < EYE_BLINK_THRESHOLD:
                    blink_detected = True
                else:
                    if blink_detected:
                        pyautogui.click()  # Perform a left mouse click on blink
                        blink_detected = False

                # Toggle eye control with 'e' key
                if keyboard.is_pressed('e'):
                    eye_control_enabled = not eye_control_enabled
                    time.sleep(0.5)  # Prevent rapid toggling

                if eye_control_enabled:
                    # Apply exponential smoothing for smoother movement
                    smoothed_x = SMOOTHING_FACTOR * previous_x + (1 - SMOOTHING_FACTOR) * avg_eye_x
                    smoothed_y = SMOOTHING_FACTOR * previous_y + (1 - SMOOTHING_FACTOR) * avg_eye_y
                    previous_x, previous_y = smoothed_x, smoothed_y

                    # Map the eye position to screen coordinates
                    screen_x, screen_y = map_to_screen(smoothed_x, smoothed_y, frame_width, frame_height)

                    # Move the mouse
                    pyautogui.moveTo(screen_x, screen_y, duration=0.1)

                # Dwell click: Trigger click if cursor stays in position for dwell_duration
                if dwell_start_time is None or (abs(previous_x - avg_eye_x) > 10 or abs(previous_y - avg_eye_y) > 10):
                    dwell_start_time = time.time()
                elif time.time() - dwell_start_time > dwell_duration:
                    pyautogui.click()
                    dwell_start_time = None  # Reset dwell timer

                # Draw visualization
                cv2.circle(frame, (int(left_eye_center_x), int(left_eye_center_y)), 5, (0, 255, 0), -1)
                cv2.circle(frame, (int(right_eye_center_x), int(right_eye_center_y)), 5, (0, 255, 0), -1)
                cv2.putText(frame, f"Eye Control: {'ON' if eye_control_enabled else 'OFF'}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if eye_control_enabled else (0, 0, 255), 2)

        # Display the frame
        cv2.imshow("Advanced Eye-Controlled Mouse", frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()


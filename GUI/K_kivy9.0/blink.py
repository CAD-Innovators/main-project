import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Blink detection parameters
blink_start_time = None
short_blink_threshold = 0.3  # Duration for short blink
long_blink_threshold = 0.5   # Duration for long blink
blink_duration = 0

def is_blink(eye_landmarks):
    # Simple blink detection by comparing the distance between two eye landmarks
    # (landmarks indices are for right eye) - This is a simplified approach
    eye_open_threshold = 0.2  # Adjust this value based on your testing
    eye_open_ratio = (eye_landmarks[3].y - eye_landmarks[1].y) / (eye_landmarks[2].y - eye_landmarks[0].y)
    return eye_open_ratio < eye_open_threshold

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB (as required by mediapipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get face mesh landmarks
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            # Draw the face mesh landmarks
            mp.solutions.drawing_utils.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

            # Extract right eye landmarks (simplified indices for the right eye)
            eye_landmarks = [
                face_landmarks.landmark[i] for i in [33, 159, 145, 133]  # Example landmarks for right eye
            ]

            if is_blink(eye_landmarks):
                if blink_start_time is None:
                    blink_start_time = time.time()  # Start timing the blink
            else:
                if blink_start_time is not None:
                    blink_duration = time.time() - blink_start_time
                    if blink_duration <= short_blink_threshold:
                        print("Short blink detected")
                    elif blink_duration >= long_blink_threshold:
                        print("Long blink detected")
                    blink_start_time = None  # Reset blink timer

    # Display the frame with facial landmarks
    cv2.imshow('Eye Blink Detection', frame)

    # Press 'q' to quit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()


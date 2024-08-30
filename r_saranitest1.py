import cv2
import dlib
import numpy as np

# Load pre-trained models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # Download from dlib's website

def detect_face_landmarks(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)
        landmarks_np = np.zeros((68, 2), dtype=int)
        
        for i in range(0, 68):
            landmarks_np[i] = (landmarks.part(i).x, landmarks.part(i).y)
        
        return face, landmarks_np
    return None, None
def extract_eye_regions(landmarks):
    left_eye = landmarks[36:42]  # Left eye landmarks
    right_eye = landmarks[42:48] # Right eye landmarks

    left_eye_rect = cv2.boundingRect(np.array(left_eye))
    right_eye_rect = cv2.boundingRect(np.array(right_eye))

    return left_eye_rect, right_eye_rect
def detect_pupil(eye_region, threshold_value):
    gray_eye = cv2.cvtColor(eye_region, cv2.COLOR_BGR2GRAY)
    _, binary_eye = cv2.threshold(gray_eye, threshold_value, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(binary_eye, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments['m00'] != 0:
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
            return (cx, cy)
    return None
def calculate_ratios(eye_center, pupil_position, eye_width, eye_height):
    HR = (pupil_position[0] - eye_center[0]) / (eye_width / 2)
    VR = (pupil_position[1] - eye_center[1]) / (eye_height / 2)
    return HR, VR
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    face, landmarks = detect_face_landmarks(frame)
    if face is not None:
        left_eye_rect, right_eye_rect = extract_eye_regions(landmarks)
        
        left_eye_region = frame[left_eye_rect[1]:left_eye_rect[1] + left_eye_rect[3], left_eye_rect[0]:left_eye_rect[0] + left_eye_rect[2]]
        right_eye_region = frame[right_eye_rect[1]:right_eye_rect[1] + right_eye_rect[3], right_eye_rect[0]:right_eye_rect[0] + right_eye_rect[2]]
        
        left_pupil = detect_pupil(left_eye_region, threshold_value=70)
        right_pupil = detect_pupil(right_eye_region, threshold_value=70)
        
        if left_pupil and right_pupil:
            left_eye_center = (left_eye_rect[2] // 2, left_eye_rect[3] // 2)
            right_eye_center = (right_eye_rect[2] // 2, right_eye_rect[3] // 2)
            
            left_HR, left_VR = calculate_ratios(left_eye_center, left_pupil, left_eye_rect[2], left_eye_rect[3])
            right_HR, right_VR = calculate_ratios(right_eye_center, right_pupil, right_eye_rect[2], right_eye_rect[3])
            
            HR = (left_HR + right_HR) / 2
            VR = (left_VR + right_VR) / 2
            
            if HR < -0.3:
                print("Looking Left")
            elif HR > 0.3:
                print("Looking Right")
            elif VR < -0.3:
                print("Looking Up")
            elif VR > 0.3:
                print("Looking Down")
            else:
                print("Looking Center")
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

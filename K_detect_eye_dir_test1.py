import cv2
import numpy as np
import dlib
import time

def eye_on_mask(mask, side, shape):
    points = [shape[i] for i in side]
    points = np.array(points, dtype=np.int32)
    mask = cv2.fillConvexPoly(mask, points, 255)
    l = points[0][0]
    t = (points[1][1] + points[2][1]) // 2
    r = points[3][0]
    b = (points[4][1] + points[5][1]) // 2
    return mask, [l, t, r, b]

def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

def euclidean_distance(leftx, lefty, rightx, righty):
    return np.sqrt((leftx - rightx) ** 2 + (lefty - righty) ** 2)

def get_EAR(eye_points, facial_landmarks):
    left_point = [facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y]
    right_point = [facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y]
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    hor_line_length = euclidean_distance(left_point[0], left_point[1], right_point[0], right_point[1])
    ver_line_length = euclidean_distance(center_top[0], center_top[1], center_bottom[0], center_bottom[1])
    EAR = ver_line_length / hor_line_length
    return EAR

def find_eyeball_position(end_points, cx, cy):
    x_ratio = (end_points[0] - cx) / (cx - end_points[2])
    y_ratio = (cy - end_points[1]) / (end_points[3] - cy)
    if x_ratio > 3:
        return "left"
    elif x_ratio < 0.33:
        return "right"
    elif y_ratio < 0.33:
        return "up"
    else:
        return "center"

def contouring(thresh, mid, img, end_points, right=False):
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if cnts:
        cnt = max(cnts, key=cv2.contourArea)
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            if right:
                cx += mid
            cv2.circle(img, (cx, cy), 4, (0, 0, 255), 2)
            pos = find_eyeball_position(end_points, cx, cy)
            return pos
    return None

def process_thresh(thresh):
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)
    thresh = cv2.medianBlur(thresh, 3)
    thresh = cv2.bitwise_not(thresh)
    return thresh

def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords

def print_eye_pos(img, left, right):
    text = ''
    if left:
        text += f"Left Eye: {left} \t"
    if right:
        text += f"Right Eye: {right}"
    return text

def detect_direction(image):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    
    left_eye_points = [36, 37, 38, 39, 40, 41]
    right_eye_points = [42, 43, 44, 45, 46, 47]
    kernel = np.ones((9, 9), np.uint8)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(image, 1)
    
    if len(rects) == 0:
        print("No faces detected.")
        return "No direction detected"
    
    for rect in rects:
        shape = predictor(image, rect)
        left_eye_ratio = get_EAR(left_eye_points, shape)
        right_eye_ratio = get_EAR(right_eye_points, shape)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
        
        if blinking_ratio < 0.20:
            print('Blink detected')
        
        shape_np = shape_to_np(shape)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        mask, end_points_left = eye_on_mask(mask, left_eye_points, shape_np)
        mask, end_points_right = eye_on_mask(mask, right_eye_points, shape_np)
        mask = cv2.dilate(mask, kernel, 5)
        
        eyes = cv2.bitwise_and(image, image, mask=mask)
        mask = (eyes == [0, 0, 0]).all(axis=2)
        eyes[mask] = [255, 255, 255]
        mid = (shape_np[42][0] + shape_np[39][0]) // 2
        eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(eyes_gray, 75, 255, cv2.THRESH_BINARY)
        thresh = process_thresh(thresh)
        
        eyeball_pos_left = contouring(thresh[:, 0:mid], mid, image, end_points_left)
        eyeball_pos_right = contouring(thresh[:, mid:], mid, image, end_points_right, True)
        
        direction = print_eye_pos(image, eyeball_pos_left, eyeball_pos_right)
        
        return direction
    
    return 'No direction detected'

def capture_image():
    cap = cv2.VideoCapture(0)
    countdown_seconds = 3

    font = cv2.FONT_HERSHEY_SIMPLEX
    frame_rate = cap.get(cv2.CAP_PROP_FPS) or 30  # Default to 30 FPS if the frame rate can't be obtained
    wait_time = int(1000 / frame_rate)  # Time between frames in milliseconds

    # Countdown loop
    for remaining_time in range(countdown_seconds, 0, -1):
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        # Overlay countdown text on the frame
        cv2.putText(frame, f'{remaining_time}', (250, 240), font, 2, (0, 0, 0), 3, cv2.LINE_AA)

        # Display the frame with countdown
        cv2.imshow('Webcam Countdown', frame)

        # Wait for a second before the next countdown step
        if cv2.waitKey(1000) & 0xFF == ord('q'):  # Wait for 1000ms (1 second)
            break

    # Capture the final frame when countdown ends
    ret, frame = cap.read()
    if ret:
        print('Countdown ended. Returning captured image.')
        cap.release()
        cv2.destroyAllWindows()
        return frame
    else:
        print('Failed to capture image after countdown.')
        cap.release()
        cv2.destroyAllWindows()
        return None


# Example usage with countdown image
if __name__ == "__main__":
    # Create a countdown image
    countdown_image = capture_image()
    
    # Detect direction from the countdown image
    direction = detect_direction(countdown_image)
    print(f'Detected direction: {direction}')

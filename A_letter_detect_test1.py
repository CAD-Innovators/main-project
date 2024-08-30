import cv2
import numpy as np
import dlib

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
        return 1
    elif x_ratio < 0.33:
        return 2
    elif y_ratio < 0.33:
        return 3
    else:
        return 0

def contouring(thresh, mid, img, end_points, right=False):
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    try:
        cnt = max(cnts, key=cv2.contourArea)
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        if right:
            cx += mid
        cv2.circle(img, (cx, cy), 4, (0, 0, 255), 2)
        pos = find_eyeball_position(end_points, cx, cy)
        return pos
    except:
        pass

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
    if left == 1:
        text = 'left'
    elif left == 2:
        text = 'right'
    elif left == 3:
        text = 'up'
    return text

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

left = [36, 37, 38, 39, 40, 41]
right = [42, 43, 44, 45, 46, 47]

kernel = np.ones((9, 9), np.uint8)

blink_counter = 0
previous_ratio = 100
movement_sequence = []

def main():
    global previous_ratio, movement_sequence
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Rotate or flip frame as needed
        image = cv2.rotate(frame, cv2.ROTATE_180)  # Rotate 180 degrees
        image = cv2.flip(frame, 1)  # Flip horizontally
        # image = cv2.flip(frame, 0)  # Flip vertically

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(image, 1)
        word2 = ''
        
        for rect in rects:
            shape = predictor(image, rect)
            left_eye_ratio = get_EAR([36, 37, 38, 39, 40, 41], shape)
            right_eye_ratio = get_EAR([42, 43, 44, 45, 46, 47], shape)
            blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
            blinking_ratio_rounded = round(blinking_ratio, 2)
            
            if blinking_ratio < 0.20:
                if previous_ratio > 0.20:
                    word2 = 'blink'
                    
            previous_ratio = blinking_ratio
            shape = shape_to_np(shape)
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            mask, end_points_left = eye_on_mask(mask, left, shape)
            mask, end_points_right = eye_on_mask(mask, right, shape)
            mask = cv2.dilate(mask, kernel, 5)
            
            eyes = cv2.bitwise_and(image, image, mask=mask)
            mask = (eyes == [0, 0, 0]).all(axis=2)
            eyes[mask] = [255, 255, 255]
            mid = int((shape[42][0] + shape[39][0]) // 2)
            eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(eyes_gray, 75, 255, cv2.THRESH_BINARY)
            thresh = process_thresh(thresh)
            
            eyeball_pos_left = contouring(thresh[:, 0:mid], mid, image, end_points_left)
            eyeball_pos_right = contouring(thresh[:, mid:], mid, image, end_points_right, True)
            
            word = print_eye_pos(image, eyeball_pos_left, eyeball_pos_right)
            
            if word2:
                print('Blink detected')
            
            if word:
                print(f'Eye position: {word}')
                movement_sequence.append(word)
                
                # Check if the sequence matches 'left', 'up', 'left'
                if len(movement_sequence) >= 3:
                    if movement_sequence[-3:] == ['left', 'up', 'left']:
                        cv2.putText(image, 'Detected: A', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        movement_sequence = []  # Reset sequence after detection
            
            # Display the image with annotations
            cv2.imshow('Eye Tracking', image)
            
            # Exit loop when 'q' is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

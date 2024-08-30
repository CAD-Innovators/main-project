import cv2
import dlib
import numpy as np
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
from scipy.spatial import distance as dist
from collections import deque

# Initialize the dlib face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Eye Aspect Ratio (EAR) threshold for detecting closed eyes
EAR_THRESHOLD = 0.2
N_FRAMES = 10  # Process every nth frame to improve accuracy

# Function to calculate Eye Aspect Ratio (EAR)
def calculate_ear(eye_points, facial_landmarks):
    p1 = facial_landmarks.part(eye_points[1])
    p2 = facial_landmarks.part(eye_points[5])
    p3 = facial_landmarks.part(eye_points[2])
    p4 = facial_landmarks.part(eye_points[4])
    p5 = facial_landmarks.part(eye_points[0])
    p6 = facial_landmarks.part(eye_points[3])

    # Compute distances between the vertical eye landmarks
    vertical_distance1 = dist.euclidean((p2.x, p2.y), (p6.x, p6.y))
    vertical_distance2 = dist.euclidean((p3.x, p3.y), (p5.x, p5.y))
    
    # Compute the distance between the horizontal eye landmarks
    horizontal_distance = dist.euclidean((p1.x, p1.y), (p4.x, p4.y))
    
    # Calculate EAR
    ear = (vertical_distance1 + vertical_distance2) / (2.0 * horizontal_distance)
    return ear

def get_eye_direction(eye_points, facial_landmarks, gray):
    # Get the coordinates of the eye region
    eye_region = np.array([(facial_landmarks.part(point).x, facial_landmarks.part(point).y) for point in eye_points])
    min_x = np.min(eye_region[:, 0])
    max_x = np.max(eye_region[:, 0])
    min_y = np.min(eye_region[:, 1])
    max_y = np.max(eye_region[:, 1])
    
    # Extract the eye image
    eye_image = gray[min_y:max_y, min_x:max_x]
    
    # Apply histogram equalization for better contrast
    eye_image = cv2.equalizeHist(eye_image)
    
    # Use adaptive thresholding
    threshold_eye = cv2.adaptiveThreshold(eye_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)
    
    # Calculate the center of mass for the thresholded eye image
    moments = cv2.moments(threshold_eye)
    if moments['m00'] != 0:
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
    else:
        cx, cy = 0, 0
    
    horizontal_direction = ""
    vertical_direction = ""

    # Determine horizontal direction
    if cx < threshold_eye.shape[1] // 3:
        horizontal_direction = "Left"
    elif cx > 2 * threshold_eye.shape[1] // 3:
        horizontal_direction = "Right"
    else:
        horizontal_direction = "Center"

    # Determine vertical direction
    if cy < threshold_eye.shape[0] // 3:
        vertical_direction = "Up"
    elif cy > 2 * threshold_eye.shape[0] // 3:
        vertical_direction = "Down"
    else:
        vertical_direction = "Center"
    
    return horizontal_direction, vertical_direction

def detect_eye_movement():
    ret, frame = cap.read()
    if not ret:
        return
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    direction_history = []
    
    for face in faces:
        landmarks = predictor(gray, face)
        
        # Detect eye directions for both eyes
        left_eye_horizontal, left_eye_vertical = get_eye_direction([36, 37, 38, 39, 40, 41], landmarks, gray)
        right_eye_horizontal, right_eye_vertical = get_eye_direction([42, 43, 44, 45, 46, 47], landmarks, gray)
        
        # Calculate EAR to check if eyes are closed
        left_ear = calculate_ear([36, 37, 38, 39, 40, 41], landmarks)
        right_ear = calculate_ear([42, 43, 44, 45, 46, 47], landmarks)
        
        if left_ear < EAR_THRESHOLD and right_ear < EAR_THRESHOLD:
            final_direction = "Eyes Closed"
        else:
            # Combine the directions
            combined_horizontal_direction = "Center"
            combined_vertical_direction = "Center"
            
            if left_eye_horizontal == right_eye_horizontal:
                combined_horizontal_direction = left_eye_horizontal
            elif "Left" in (left_eye_horizontal, right_eye_horizontal):
                combined_horizontal_direction = "Left"
            elif "Right" in (left_eye_horizontal, right_eye_horizontal):
                combined_horizontal_direction = "Right"
            
            if left_eye_vertical == right_eye_vertical:
                combined_vertical_direction = left_eye_vertical
            elif "Up" in (left_eye_vertical, right_eye_vertical):
                combined_vertical_direction = "Up"
            elif "Down" in (left_eye_vertical, right_eye_vertical):
                combined_vertical_direction = "Down"
            
            # Determine final eye movement direction
            final_direction = f"{combined_horizontal_direction}-{combined_vertical_direction}"
            if final_direction == "Center-Center":
                final_direction = "Center"
        
        # Add the detected direction to the history
        direction_history.append(final_direction)
    
    # Use majority voting over the last N frames to stabilize the detection
    if len(direction_history) >= N_FRAMES:
        direction_history = direction_history[-N_FRAMES:]
        final_direction = max(set(direction_history), key=direction_history.count)
    else:
        final_direction = "No Movement Detected"
    
    # Display the direction on the GUI
    result_label.config(text=final_direction)
    
    # Convert the frame to a format Tkinter can display
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    camera_label.imgtk = imgtk
    camera_label.configure(image=imgtk)
    
    # Repeat the function after 10ms
    camera_label.after(10, detect_eye_movement)

# Initialize Tkinter window
window = tk.Tk()
window.title("Eye Movement Detection")

# Create a label to show the camera feed
camera_label = Label(window)
camera_label.pack()

# Create a label to show the results
result_label = Label(window, text="", font=("Helvetica", 16))
result_label.pack()

# Create a button to start the eye movement detection
start_button = Button(window, text="Start Detection", command=detect_eye_movement)
start_button.pack()

# Initialize the camera
cap = cv2.VideoCapture(0)

# Start the Tkinter event loop
window.mainloop()

# Release the camera when the window is closed
cap.release()
cv2.destroyAllWindows()

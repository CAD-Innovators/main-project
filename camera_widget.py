from kivy.uix.floatlayout import FloatLayout
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image

class CameraWidget(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create an Image widget to display the camera feed
        self.img_widget = Image(allow_stretch=True, keep_ratio=True)
        self.add_widget(self.img_widget)

        # Open the default camera (usually the webcam)
        self.capture = cv2.VideoCapture(0)

        # Schedule the update method to run every frame (1/30th of a second or so)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        # Read the frame from the camera
        ret, frame = self.capture.read()
        if ret:
            # Flip the frame vertically (use 0 for horizontal, -1 for both horizontal and vertical)
            frame = cv2.flip(frame, 0)

            # Convert it from BGR to RGB (because OpenCV uses BGR and Kivy uses RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get the image shape and update the Kivy Texture
            buf1 = frame.flatten()
            buf = bytes(buf1)
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            image_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

            # Display the image on the Image widget
            self.img_widget.texture = image_texture

    def on_stop(self):
        # Release the camera when the app is closed
        self.capture.release()


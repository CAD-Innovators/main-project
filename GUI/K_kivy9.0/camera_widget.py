from kivy.uix.floatlayout import FloatLayout
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
import eye_direction as EyeDir

class CameraWidget(FloatLayout):
    
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        self.img_widget = self.ids.camera_feed
        self.countdown_seconds = 3  # Initialize countdown seconds
        self.countdown_event = None

        # Start the countdown
        self.start_countdown()

    def start_countdown(self):
        # Schedule countdown to update every second
        self.countdown_event = Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        # Countdown logic
        if self.countdown_seconds > 0:
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.flip(frame, 0)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Display countdown on frame
                cv2.putText(frame, f"Starting in {self.countdown_seconds}...", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Update texture for the countdown
                buf1 = frame.flatten()
                buf = bytes(buf1)
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                image_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                self.img_widget.texture = image_texture

            # Decrease the countdown
            self.countdown_seconds -= 1
        else:
            # Stop the countdown event after it's done
            if self.countdown_event:
                self.countdown_event.cancel()

            # Start the camera feed normally after countdown ends
            Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 0)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            buf1 = frame.flatten()
            buf = bytes(buf1)
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            image_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.img_widget.texture = image_texture

            # Get eye direction and update the label
            direction = EyeDir.detect_eye_direction(frame)
            self.ids.direction_label.text = f"Direction: {direction}"

    def on_stop(self):
        self.capture.release()
        cv2.destroyAllWindows()
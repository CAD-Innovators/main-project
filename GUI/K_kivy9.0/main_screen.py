from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from emergency_widget import EmergencyWidget
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

class MainScreen(Screen):
    
    is_emergency_visible = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.emergency_widget = EmergencyWidget()
        self.add_widget(self.emergency_widget)  # Add the emergency widget to the main screen

        self.emergency_sound = SoundLoader.load('bleep.mp3')

    def on_enter(self):
        # Bind the left and right arrow keys to switch between screens
        Window.bind(on_key_down=self.on_key_down)

    def on_leave(self):
        # Unbind the keyboard events when leaving the screen
        Window.unbind(on_key_down=self.on_key_down)

    def show_emergency_widget(self):
        self.emergency_widget.show()  # Show the emergency widget
        self.is_emergency_visible = True

    def hide_emergency_widget(self):
        self.emergency_widget.hide()  # Hide the emergency widget
        self.is_emergency_visible = False

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if self.emergency_widget.opacity == 0:  # Only allow transitions when the widget is hidden
            if key == 276:  # Left arrow key
                self.manager.current = 'keyboard'  # Slide to Keyboard screen
            elif key == 275:  # Right arrow key
                self.manager.current = 'iot'  # Slide to IoT screen
            elif key == 273:  # Up arrow key
                self.show_emergency_widget()  # Show the emergency widget
        else:  # If the emergency widget is visible
            if key == 275:  # If the right arrow key is pressed when emergency is active
                if self.emergency_sound:
                    self.emergency_sound.play()  # Play the emergency audio
            elif key == 276 or key == 273 :  # Left arrow key
                # Stop the emergency sound if it is currently playing
                if self.emergency_sound and self.emergency_sound.state == 'play':
                    self.emergency_sound.stop()  # Stop the emergency sound
                self.hide_emergency_widget()
            elif key == 273:
                self.hide_emergency_widget()  # Hide the emergency widget
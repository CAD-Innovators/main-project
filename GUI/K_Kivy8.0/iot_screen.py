from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

class IoTScreen(Screen):
    def __init__(self, **kwargs):
        super(IoTScreen, self).__init__(**kwargs)

        self.selected_device = None  # Track which device is selected
        self.fan_state = 'off'  # Track the current state of the fan
        self.light_state = 'off'  # Track the current state of the light

        # Create a layout for the buttons
        self.layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.5))

        # Create the fan image (initially hidden)
        self.fan_image = Image(source='Images/OFF.png', size_hint=(0.5, 0.80))  # Takes half of the width
        self.layout.add_widget(self.fan_image)

        # Create the light image (initially hidden)
        self.light_image = Image(source='Images/OFF.png', size_hint=(0.5, 0.80))  # Takes half of the width
        self.layout.add_widget(self.light_image)

        # Add the layout to the IoT screen
        self.add_widget(self.layout)

    def on_enter(self):
        self.fan_state = 'off'
        self.light_state = 'off'
        self.fan_image.source = 'Images/OFF.png'  # Ensure the fan image shows OFF
        self.light_image.source = 'Images/OFF.png'  # Ensure the light image shows OFF
        self.selected_device = None  # Reset selected device
        Window.bind(on_key_down=self.on_key_down)

    def on_leave(self):
        Window.unbind(on_key_down=self.on_key_down)

    def go_home(self):
        self.manager.current = 'main'

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 273:  # Up arrow key
            self.manager.current = 'main'
        elif key == 276:  # Left arrow key - toggle fan
            if self.selected_device == 'fan':
                self.toggle_fan()
            else:
                self.select_device('fan')  # Select fan if not already selected
        elif key == 275:  # Right arrow key - toggle light
            if self.selected_device == 'light':
                self.toggle_light()
            else:
                self.select_device('light')  # Select light if not already selected

    def select_device(self, device):

        self.ids.fan_button.background_color = 0.900, 0.600, 0.906, 1  # light purple
        self.ids.light_button.background_color = 0.6471, 0.3804, 0.8353, 1  # light violet

        if device == 'fan':
            self.ids.fan_button.background_color = 0.6627, 0.3255, 0.6784, 1  # Change FAN button color
            self.selected_device = 'fan'
            self.fan_image.opacity = 1  # Show fan image
            self.light_image.opacity = 1  # Hide light image
        elif device == 'light':
            self.ids.light_button.background_color = 0.5545, 0.3255, 0.6984, 1  # Change LIGHT button color
            self.selected_device = 'light'
            self.fan_image.opacity = 1  # Hide fan image
            self.light_image.opacity = 1  # Show light image

    def toggle_fan(self):
        self.fan_state = 'on' if self.fan_state == 'off' else 'off'
        self.fan_image.source = 'Images/ON.png' if self.fan_state == 'on' else 'Images/OFF.png'
        self.fan_image.reload()  # Reload the image to reflect the change

    def toggle_light(self):
        self.light_state = 'on' if self.light_state == 'off' else 'off'
        self.light_image.source = 'Images/ON.png' if self.light_state == 'on' else 'Images/OFF.png'
        self.light_image.reload()  # Reload the image to reflect the change


'''For kv file in case for future-use
            Label:
                text: 'REMOTE MODE'  # Header text
                font_size: 32  # Smaller font size
                size_hint_y: None  # Allow manual height specification
                #height: 0  # Height of the header
                halign: 'left'  # Align the text horizontally
                valign: 'middle'  # Align the text vertically
                text_size: self.size  # Set text size to the label size for proper alignment
                color: 0.3, 0.3, 0.3, 1  # Dark gray color (RGBA)
                padding: [50, 0, 0, 0]  # Add padding above the text for space below
'''
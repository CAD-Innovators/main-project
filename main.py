from kivy.app import App
from main_screen import MainScreen
from keyboard_screen import KeyboardScreen
from iot_screen import IoTScreen
from help_screen import HelpScreen
from type_screen import TypeScreen
from camera_widget import CameraWidget

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout


class ProjectApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(KeyboardScreen(name='keyboard'))
        sm.add_widget(IoTScreen(name='iot'))
        sm.add_widget(TypeScreen(name='type'))  # Add TypeScreen here
        sm.add_widget(HelpScreen(name='help'))
    
        sm.current = 'main'  # Set the default screen to main

        # Create the main layout
        root = FloatLayout(orientation='vertical')

        # Add the ScreenManager to the layout
        root.add_widget(sm)

        # Create and add the CameraWidget, make it float on top
        camera_widget = CameraWidget(size_hint=(0.3, 0.3), pos_hint={'x': 0.5, 'y': 0.5})
        root.add_widget(camera_widget)

        return root


if __name__ == '__main__':
    ProjectApp().run()
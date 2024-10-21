from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


# ScreenOne class
class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # Button to pass data and move to ScreenTwo
        self.button = Button(text='Go to Screen Two')
        self.button.bind(on_release=self.pass_data)

        # Add widgets to the layout
        self.layout.add_widget(self.button)
        self.add_widget(self.layout)

    def pass_data(self, instance):
        # Store data in the App class
        App.get_running_app().shared_data = "Data from Screen One"
        # Navigate to ScreenTwo
        self.manager.current = 'screen_two'


# ScreenTwo class
class ScreenTwo(Screen):
    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # Label to display received data
        self.data_label = Label(text="Waiting for data...")

        # Button to go back to ScreenOne
        self.back_button = Button(text='Go Back to Screen One')
        self.back_button.bind(on_release=self.go_back)

        # Add widgets to the layout
        self.layout.add_widget(self.data_label)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

    def on_enter(self, *args):
        # When entering the screen, display the shared data
        shared_data = App.get_running_app().shared_data
        self.data_label.text = f"Received data: {shared_data}"

    def go_back(self, instance):
        # Navigate back to ScreenOne
        self.manager.current = 'screen_one'


# MyScreenManager class
class MyScreenManager(ScreenManager):
    pass


# Main App class
class MyApp(App):
    shared_data = None  # Shared data between screens

    def build(self):
        sm = MyScreenManager()
        sm.add_widget(ScreenOne(name='screen_one'))
        sm.add_widget(ScreenTwo(name='screen_two'))
        return sm


# Run the application
if __name__ == '__main__':
    MyApp().run()

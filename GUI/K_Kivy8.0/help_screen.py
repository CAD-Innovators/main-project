from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

class HelpScreen(Screen):
    def on_enter(self):
        # Bind the key down event when the screen is entered
        Window.bind(on_key_down=self.on_key_down)

    def on_leave(self):
        # Unbind the key down event when leaving the screen
        Window.unbind(on_key_down=self.on_key_down)

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 273:  # Up arrow key
            self.manager.current = 'type'
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from list_widget import ListWidget
from kivy.properties import ObjectProperty
from speech import speak_phrase
from kivymd.app import MDApp
from kivy_garden.xcamera import XCamera
from search_widget import SearchWidget 

class TypeScreen(Screen):
    list_widget = None  # Reference to the ListWidget
    search_widget = None  # Reference to the SearchWidget
    typing_widget = ObjectProperty(None)  # Reference to the TextInput widget
    
    def __init__(self, **kwargs):
        super(TypeScreen, self).__init__(**kwargs)

        self.list_widget = ListWidget()  # Create an instance of ListWidget
        self.search_widget = SearchWidget()  # Create an instance of SearchWidget

        self.add_widget(self.list_widget)  # Add ListWidget to the screen
        self.add_widget(self.search_widget)  # Add SearchWidget to the screen

        self.hide_list_widget()  # Ensure it's hidden by default
        self.hide_search_widget()

        self.browser = None

    def show_list_widget(self):
        self.list_widget.show()  # Show the list widget
        self.list_widget.highlight_current_phrase()  # Highlight the first phrase

    def hide_list_widget(self):
        self.list_widget.hide()  # Hide the list widget

    def show_search_widget(self):
        self.search_widget.opacity = 1

    def hide_search_widget(self):
        self.search_widget.opacity = 0
        self.search_widget.size_hint_y = 0

    def on_enter(self):
        Window.bind(on_key_down=self.on_key_down)  # Bind keyboard events on entering screen

    def on_leave(self):
        Window.unbind(on_key_down=self.on_key_down)  # Unbind keyboard events when leaving screen

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if self.list_widget.opacity == 0:  # If ListWidget is hidden
            if key == 275:  # Right arrow key pressed
                self.show_list_widget()  # Show ListWidget when pressing right arrow
            elif key == 273:  # Up arrow key
                # Handle other screen transitions if necessary
                self.manager.current="main"
            elif key == 276: # Left arrow key
                self.manager.current="keyboard"
            elif key == 274:  # Down arrow key
                self.manager.current="help"
                
        else:
            self.list_widget.on_key_down(window, key, scancode, codepoint, modifier, self)  # Forward key events to ListWidget

    def get_typing_widget_text(self):
        """This function retrieves the text from the TextInput widget."""
        user_input = self.typing_widget.text
        return user_input
        
    def speak_user_input(self):
        """Retrieve the text from the TextInput and use the TTS function to speak it."""
        user_input = self.get_typing_widget_text()
        if user_input.strip():  # Ensure there is input to speak
            speak_phrase(user_input)  # Use the TTS function to speak the input
        else:
            print("No input to speak.")  # Optionally handle the case where there's no input

    def search(self):
        # Hide ListWidget and show SearchWidget when 'Search' is pressed
        self.hide_list_widget()
        self.show_search_widget()
        
        # Get the search query from the input widget
        search_query = self.get_typing_widget_text()
        
        if search_query:
            # Call on_search and pass the search query to it
            #SearchWidget.on_search(search_query)
            self.search_widget.on_search(search_query)
        else:
            print("No search query entered.")

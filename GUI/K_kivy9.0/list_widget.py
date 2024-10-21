from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
from speech import speak_phrase  # Assuming you have a separate speech module

class ListWidget(FloatLayout):
    is_list_visible = BooleanProperty(False)  # Controls whether the list is visible
    current_phrase_index = 4  # Start from the first index

    def __init__(self, **kwargs):
        super(ListWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.opacity = 0  # Start hidden

    def show(self):
        self.opacity = 1  # Make visible
        self.is_list_visible = True  # Update flag

    def hide(self):
        self.opacity = 0  # Make hidden
        self.is_list_visible = False  # Update flag

    def speak_phrase(self, phrase):
        # Call your TTS or phrase-speaking function here
        speak_phrase(phrase)  # Ensure you replace this with the correct function

    
    def highlight_current_phrase(self):
        # Clear previous highlights
        buttons = [button for button in self.ids.grid_layout1.children if hasattr(button, 'text')]
        for i, button in enumerate(buttons):
            # Reset to alternating colors
            button.background_color = (0.85, 0.92, 1, 1) if i % 2 == 0 else (0.7, 0.85, 0.9, 1)

        # Highlight the current phrase
        if 0 <= self.current_phrase_index < len(buttons):
            button = buttons[self.current_phrase_index]
            button.background_color = (1, 1, 0, 1)  # Yellow for highlighting

    def actions_for_list(self, type_screen):
        # Get the current phrase and speak it
        buttons = [button for button in self.ids.grid_layout1.children if hasattr(button, 'text')]
        if 0 <= self.current_phrase_index < len(buttons):
            button = buttons[self.current_phrase_index]
            if button.text == "Speak":  # If the "Speak" button is highlighted
                type_screen.speak_user_input()  # Call the speak function from TypeScreen
            if button.text == "Search":
                type_screen.search()  # Call the search function
                
    def on_key_down(self, window, key, scancode, codepoint, modifier, type_screen):
        if self.is_list_visible:  # If the list is visible, handle list navigation
            if key == 275:  # Right arrow key (speak current phrase)
                self.actions_for_list(type_screen)
            elif key == 274:  # Down arrow key (move to next phrase)
                self.current_phrase_index = (self.current_phrase_index - 1) % 5  # Assuming 4 phrases
                self.highlight_current_phrase()  # Highlight next phrase
            elif key == 276 or key == 273:  # Left arrow or Up arrow (hide the list)
                self.hide()  # Hide the list widget
        else:
            if key == 275:  # Right arrow key to show the list widget
                self.show()  # Show the list widget
                self.highlight_current_phrase()  # Highlight the first phrase
            elif key in (276, 273):  # Left or Up arrow key to close the browser
                # Check if the search widget is present
                if type_screen.search_widget:  # Check if the SearchWidget is visible
                    type_screen.hide_search_widget()

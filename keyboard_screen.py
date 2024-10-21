from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from speech import speak_phrase  # Import the speak_phrase function
from kivy.animation import Animation
from kivy.uix.button import Button

class KeyboardScreen(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set the initial size hints for the BoxLayouts
        #self.current_phrase_index = 0
        self.left_box_size_hint = 0.5
        self.right_box_size_hint = 0.5

    def on_enter(self):
        # Bind the left and right arrow keys to switch between screens
        Window.bind(on_key_down=self.on_key_down)
        
        # Calculate total phrases dynamically based on grid layout's children
        grid_layout = self.ids.grid_layout
        buttons = sorted(grid_layout.children, key=lambda x: x.y)  # Sort by y position
        total_phrases = len(buttons)  # Get total number of buttons

        if total_phrases > 0:
            self.current_phrase_index = total_phrases - 1  # Set to the last button index
            self.highlight_current_phrase()  # Highlight the last phrase initially

        self.update_box_layouts()  # Set initial sizes
        # Set initial visibility of basic_phrase and grid_layout
        self.ids.basic_phrase.opacity = 1  # Show basic_phrase initially
        self.ids.grid_layout.opacity = 0   # Hide the grid layout initially

    def on_leave(self):
        # Unbind the keyboard events when leaving the screen
        Window.unbind(on_key_down=self.on_key_down)

    def speak_phrase(self, phrase):
        # Call the imported speak_phrase function
        speak_phrase(phrase)  # Replace this with your TTS function

    def go_home(self):
        # Navigate back to home screen
        self.manager.current = 'main'

    def type_new_page(self):
        # Example of navigating to another page for typing
        pass

    def hide_home_button(self):
        # Hide the home button initially
        home_button = self.ids.home_button  # Replace with your actual home button id
        home_button.opacity = 0  # Hide the button

    def show_home_button(self):
        # Show the home button
        home_button = self.ids.home_button  # Replace with your actual home button id
        home_button.opacity = 1  # Show the button

    def navigate_phrases(self, direction):
        # Get total number of phrases dynamically based on grid layout's children
        grid_layout = self.ids.grid_layout
        buttons = sorted(grid_layout.children, key=lambda x: x.y)
        total_phrases = len(buttons)

        # Update the current phrase index within the valid range
        self.current_phrase_index = (self.current_phrase_index + direction) % total_phrases

        # Highlight the new current phrase
        self.highlight_current_phrase()

    def highlight_current_phrase(self):
        # Clear previous highlights
        buttons = sorted(self.ids.grid_layout.children, key=lambda x: x.y)  # Sort by y position
        buttons = [button for button in buttons if hasattr(button, 'text')]  # Ensure we only get buttons

        # Get the current window size
        window_size = Window.size
        
        # Check if the window is in full-screen mode
        is_full_screen = (window_size[0] >= 1500 and window_size[1] >= 800)
        # Determine the highlighted image based on full screen
        highlight_image = 'Images/HIGHLIGHTED_PHRASE.png' if is_full_screen else 'Images/HIGHLIGHTED_PHRASE_SMALL.png'
    
        for i, button in enumerate(buttons):
            # Reset all buttons to their original background image based on their index (odd/even)
            button.background_normal = 'Images/PHRASE.png' if i % 2 == 0 else 'Images/PHRASE_ALT.png'

        # Highlight the current phrase by changing its background image
        if 0 <= self.current_phrase_index < len(buttons) and self.left_box_size_hint == 0.2:
            button = buttons[self.current_phrase_index]
            button.background_normal = highlight_image  # Change to the highlighted image
            # Scroll to the highlighted phrase
            self.scroll_to_element(button)

    def clear_highlights(self):
        # Clear any highlighted buttons
        buttons = sorted(self.ids.grid_layout.children, key=lambda x: x.y)  # Sort by y position
        buttons = [button for button in buttons if hasattr(button, 'text')]

        for i, button in enumerate(buttons):
            # Reset all buttons to their original background image based on their index (odd/even)
            button.background_normal = 'Images/PHRASE.png' if i % 2 == 0 else 'Images/PHRASE_ALT.png'

    def update_box_layouts(self):
        # Update size hints for both BoxLayouts based on current state
        left_box = self.ids.left_box  # Assuming you have ids for your BoxLayouts in the KV file
        right_box = self.ids.right_box
        
        left_box.size_hint_x = self.left_box_size_hint
        right_box.size_hint_x = self.right_box_size_hint

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 273:  # Up arrow key
            if self.left_box_size_hint == 0.5:  # In the 0.5-0.5 position
                self.go_home()  # Go to home screen
            else:
                self.navigate_phrases(1)  # Select the above button
                
        elif key == 276:  # Left arrow key
            if self.left_box_size_hint == 0.5:  # If in 0.5-0.5 position
                self.manager.current = 'type'  # Go to the Type screen
            else:
                # Move back to 0.5-0.5 position
                self.left_box_size_hint = 0.5
                self.right_box_size_hint = 0.5
                self.current_phrase_index = len(self.ids.grid_layout.children) - 1  # Highlight the last button
                self.highlight_current_phrase()  # Highlight the last button
                self.update_box_layouts()  # Update box sizes
                self.show_home_button()
                self.ids.grid_layout.opacity = 0
                self.ids.basic_phrase.opacity = 1
                self.ids.left_text.text = 'TYPE\nNEW'


        elif key == 275:  # Right arrow key
            if self.left_box_size_hint == 0.5:  # If in 0.5-0.5 position
                # Move to 0.2-0.8 position
                self.left_box_size_hint = 0.2
                self.right_box_size_hint = 0.8
                self.current_phrase_index = len(self.ids.grid_layout.children) - 1  # Highlight the last button
                self.highlight_current_phrase()  # Highlight the last button
                self.update_box_layouts()  # Update box sizes
                self.hide_home_button()
                self.ids.grid_layout.opacity = 1
                self.ids.basic_phrase.opacity = 0
                self.ids.left_text.text = ' '
                # Scroll to the last highlighted button
                self.scroll_to_element(self.ids.grid_layout.children[-1])
            else:
                # Speak the currently highlighted phrase
                self.speak_current_phrase()

        elif key == 274:  # Down arrow key
            if self.left_box_size_hint == 0.2:  # If in 0.2-0.8 position
                self.navigate_phrases(-1)  # Cycle through phrases

    def speak_current_phrase(self):
        # Speak the currently highlighted phrase
        buttons = sorted(self.ids.grid_layout.children, key=lambda x: x.y)  # Sort by y position
        buttons = [button for button in buttons if hasattr(button, 'text')]  # Ensure we only get buttons

        if 0 <= self.current_phrase_index < len(buttons):
            button = buttons[self.current_phrase_index]
            self.speak_phrase(button.text)  # Speak the highlighted phrase

    def scroll_to_element(self, widget):
        # Get the scroll view and grid layout
        scroll_view = self.ids.scroll_view
        grid_layout = self.ids.grid_layout

        # Calculate the widget's position in the grid
        widget_y = widget.y  # Y position of the widget in the grid
        widget_height = widget.height  # Height of the widget
        scroll_view_height = scroll_view.height  # Height of the ScrollView

        # Calculate the total height of the grid layout
        total_grid_height = grid_layout.height

        # Check if the widget is outside the visible area of the ScrollView
        if widget_y < (scroll_view_height * scroll_view.scroll_y) or (widget_y + widget_height) > (scroll_view_height * scroll_view.scroll_y + scroll_view_height):
            # Calculate the scroll position to bring the widget into view
            target_scroll_y = (widget_y) / total_grid_height
            # Use Animation for smooth scrolling
            animation = Animation(scroll_y=min(max(0, target_scroll_y), 1), duration=0.3)  # Adjust duration for speed
            animation.start(scroll_view)

    def get_basic_phrases(self):
        # Get the grid layout widget by its ID
        grid_layout = self.root.ids.grid_layout
        
        # List to store the button texts
        phrases = []
        
        # Loop through all the children of the grid_layout
        for child in grid_layout.children:
            # Check if the child is a Button
            if isinstance(child, Button):
                # Add the button text to the list
                phrases.append(child.text)
        
        return phrases

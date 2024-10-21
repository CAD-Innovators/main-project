import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window  # Import to capture keyboard events
import webview  # PyWebView for displaying the web content
import requests  # For API requests to SerpAPI

class SearchResults(BoxLayout):
    def __init__(self, **kwargs):
        super(SearchResults, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.webview_opened = False  # Track if the webview is currently opened

    def display_results(self, results):
        # Clear any existing widgets (results from previous searches)
        self.clear_widgets()

        # Create a ScrollView for results
        scrollview = ScrollView(size_hint=(1, 1), bar_width=10)
        results_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        results_layout.bind(minimum_height=results_layout.setter('height'))

        # Add each result to the layout
        for result in results:
            title = result.get('title')
            link = result.get('link')
            snippet = result.get('snippet')

            # Clickable Title
            title_label = Label(
                text=f"[b][ref={link}]{title}[/ref][/b]", markup=True, size_hint_y=None, height=40
            )
            title_label.bind(on_ref_press=self.on_ref_press)
            snippet_label = Label(text=snippet, size_hint_y=None, height=60)

            # Add title and snippet to the layout
            results_layout.add_widget(title_label)
            results_layout.add_widget(snippet_label)

        scrollview.add_widget(results_layout)
        self.add_widget(scrollview)

    def on_ref_press(self, instance, link):
        # When a link is clicked, open it in PyWebView inside the app
        webview.create_window('Search Result', link)
        webview.start()  # This will open the link in a PyWebView window
        self.webview_opened = True  # Mark the webview as opened

class SearchApp(App):
    def build(self):
        # Main layout to hold the input and results
        main_layout = BoxLayout(orientation='vertical', spacing=10)

        # Text input for search queries
        self.search_input = TextInput(
            hint_text="Enter search query",
            size_hint=(1, 0.1),
            multiline=False
        )
        main_layout.add_widget(self.search_input)

        # Search button
        search_button = Button(
            text="Search",
            size_hint=(1, 0.1)
        )
        search_button.bind(on_press=self.perform_search)
        main_layout.add_widget(search_button)

        # Search results layout
        self.results_layout = SearchResults(size_hint=(1, 0.8))
        main_layout.add_widget(self.results_layout)

        # Bind keyboard events
        Window.bind(on_key_down=self.on_key_down)

        return main_layout

    def perform_search(self, instance):
        query = self.search_input.text.strip()
        if query:
            # Fetch actual search results from SerpAPI
            api_key = 'd7aad7ad93417f4edc48782a59b7b3a14650f1c4b672b0b9e7d1ad0eeeb16a01'  # Replace with your SerpAPI key
            url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}"
            response = requests.get(url)
            data = response.json()

            # Extract search results
            results = []
            for result in data.get("organic_results", []):
                results.append({
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': result.get('snippet', '')
                })

            # Display the search results in the app
            self.results_layout.display_results(results)
        else:
            print("No query entered")

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key in (37, 39):  # Left (37) and Right (39) arrow keys
            if self.results_layout.webview_opened:
                # Close the webview if it's open and an arrow key is pressed
                webview.destroy_window()
                self.results_layout.webview_opened = False  # Mark webview as closed
            else:
                # Clear search results if no webview is open
                self.results_layout.clear_widgets()  # Close results on arrow key press


if __name__ == "__main__":
    SearchApp().run()

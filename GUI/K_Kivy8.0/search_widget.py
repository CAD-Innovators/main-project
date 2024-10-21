from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

class SearchWidget(BoxLayout):
    
    

    
    def on_search(self, query):
        
        if query:
            # Replace with your actual SerpAPI key
            api_key = 'd7aad7ad93417f4edc48782a59b7b3a14650f1c4b672b0b9e7d1ad0eeeb16a01'  
            url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}"
            
            try:
                # Make a GET request to the SerpAPI
                response = requests.get(url)
                data = response.json()

                # Check if the request was successful
                if response.status_code == 200:
                    # Extract the search results
                    results = data.get("organic_results", [])
                    if results:
                        # Format the results for display
                        result_text = "\n".join([f"{result.get('title')}: {result.get('snippet', '')}" for result in results])
                        self.ids.results_label.text = f"Results for: {query}\n\n{result_text}"
                    else:
                        self.ids.results_label.text = "No results found."
                else:
                    self.ids.results_label.text = "Error fetching results."

            except Exception as e:
                self.ids.results_label.text = f"An error occurred: {str(e)}"
        else:
            self.ids.results_label.text = "Please enter a search query."


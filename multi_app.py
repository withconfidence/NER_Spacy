import streamlit as st


class MultiApp:
    def __init__(self):
        self.pages = []

    def add_app(self, title, func):
        """Adds a new application."""
        self.pages.append({

            "title": title,
            "function": func
        })

    def run(self):
        # Dropdown to select the page to run
        page = st.sidebar.selectbox(
            'App Navigation',
            self.pages,
            format_func=lambda page: page['title']
        )

        # run the app function
        page['function']()

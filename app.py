import streamlit as st
from multi_app import MultiApp
from apps import model, tagging, home

app = MultiApp()

st.markdown("""
This is a demo for text tagging and annotation model training.

""")

app.add_app("HOME", home.app)
app.add_app("Annotation", tagging.app)
app.add_app("Training", model.app)

# the main app
app.run()

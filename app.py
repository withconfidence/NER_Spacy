import streamlit as st
from multi_app import MultiApp
from apps import model, annotation, tagging, home

app = MultiApp()

st.markdown("""
This is a demo for text tagging and annotation model training.

""")

app.add_app("HOME", home.app)
app.add_app("Auto-Annotation", tagging.app)
app.add_app("New Annotation", annotation.app)
app.add_app("Training", model.app)

# the main app
app.run()

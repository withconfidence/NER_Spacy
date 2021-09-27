import streamlit as st


def app():
    st.title("How to use this app?")
    st.header("Steps:")
    st.write("This app consists of 2 steps for annotation and training.")
    st.write("The followings are the workflow.")

    st.header("Annotation:")
    st.write("Go to 'Annotation' page in the navigation, and follow the steps to get"
             " text annotated and save it into JSON file.")

    st.header("Training:")
    st.write("Go to 'Training' page in the navigation.")
    st.write("Choose JSON file that you saved in Annotation page, and follow other steps.")

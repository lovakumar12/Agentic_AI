import streamlit as st

st.title("Simple Test App")
st.write("If this works, then Streamlit is running properly")
name = st.text_input("Enter your name")
if name:
    st.write(f"Hello, {name}!")

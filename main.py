
import matplotlib.pyplot as plt
import streamlit as st

st.header('st.button')
if st.button('Say hello'):
    st.write('why you saying hello?')
else:
    st.write('Goodbye')

st.write('Hello world')
st.title("Hello Streamlit-er")
st.markdown(
    """This is a playground for us
    
    """
)
import streamlit as st

def contact_info():
    st.title("Contact Information")

    st.subheader("Email:")
    st.write("awanishyadav967@gmail.com")

    st.subheader("GitHub:")
    st.write("https://github.com/awanishyadav967")

    st.subheader("Linkedin:")
    st.write("https://www.linkedin.com/in/avanish-yadav-a1a062224/")

    st.subheader("Feel free to explore more of my Streamlit projects:")


    st.write("[Multiple Disease Prediction App](https://awanishyadav967-disease-prediction-project-mdps-public-g8edal.streamlit.app/")
    st.write("[Hate Speech Detection](https://hate-speech1234-xo1ki5cdf1l.streamlit.app/")
    st.write("[Stock Market Prediction](https://stockpricepredictor1234.streamlit.app/")
    st.write("[Cyclone Speed detection](https://awanishyadav967-cyclonespeed-prediction-main-ph86ib.streamlit.app/")



def app():
    contact_info()

if __name__ == "__main__":
    app()

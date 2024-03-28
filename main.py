import streamlit as st
from streamlit_option_menu import option_menu
import feedback,home, about,contact


st.set_page_config(
    page_title="MDF Model",
)

def run_app(option):
    if option == "Home":
        home.app()
    elif option == "Feedback":
        feedback.app()
    elif option == "About":
        about.app()
    elif option == "Contact":
        contact.app()

#st.title("MDF Model")

with st.sidebar:
    option = option_menu(
        menu_title='Navigation',
        options=['Feedback','Home' , 'About', 'Contact'],

          icons=['trophy-fill','house-fill','person-circle','chat-fill','info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"},
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
    )

run_app(option)

import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_feedback_email(name, feedback_message, satisfaction_level, recipient_email, additional_comment=""):
    # Email configuration
    sender_email = "awanishyadav967@gmail.com"
    password = "zzah giku zpbi zpit"

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Feedback Received"

    # Email content
    body = f"Name: {name}\nFeedback Message: {feedback_message}\nSatisfaction Level: {satisfaction_level}"
    if additional_comment:
        body += f"\nAdditional Comment: {additional_comment}"

    msg.attach(MIMEText(body, 'plain'))

    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def feedback_form():
    st.title("Feedback Form")

    st.write("We value your feedback! Please fill out the form below:")

    # Text input for the user's name
    name = st.text_input("Your Name")

     # Text input for recipient email
    recipient_email = st.text_input("Email", help="Enter Your's email address")

    # Text area for feedback message
    feedback_message = st.text_area("Feedback Message", height=150)

    # Rating scale for satisfaction level
    satisfaction_level = st.slider("Satisfaction Level[Optional]", min_value=0, max_value=10, step=1)

    # Checkbox for additional comments
    additional_comments = st.checkbox("I have additional comments")


    #If user donot want to give additional comment
    additional_comment = ""

    if additional_comments:
        additional_comment = st.text_area("Additional Comments", height=100)

    # Button to submit feedback
    if st.button("Submit Feedback"):
        # Send feedback via email
        send_feedback_email(name, feedback_message, satisfaction_level, recipient_email, additional_comment)
        st.success("Feedback submitted successfully!")

def app():
    feedback_form()

if __name__ == "__main__":
    app()

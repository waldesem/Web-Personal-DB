import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = '0.0.0.0'
SMTP_PORT = 587
SMTP_USERNAME = 'your_username'
SMTP_PASSWORD = 'your_password'
SENDER_EMAIL = 'staffsec@example.com'


def send_text_email(receiver_email, subject, message):
    # Create a MIME message object
    msg = MIMEMultipart()
    
    # Set the sender and receiver email addresses
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    # Create a plain text part for the email body
    text_part = MIMEText(message, 'plain')
    
    # Attach the plain text part to the message object
    msg.attach(text_part)
    
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        # Start TLS encryption (optional)
        server.starttls()
        
        # Login to the email account
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Send the email
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        
        return "Email sent successfully!"
    except Exception as e:
        return f"An error occurred while sending the email: {str(e)}"
    finally:
        # Close the connection to the SMTP server
        server.quit()

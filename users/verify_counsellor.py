
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
def verify(email):
    html_content="""
                <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>Verification in Progress</title>
            <style>
                body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                }
                .container {
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                .header {
                text-align: center;
                padding: 10px 0;
                }
                .header img {
                width: 100px;
                }
                .content {
                padding: 20px;
                text-align: center;
                }
                .content h1 {
                font-size: 24px;
                margin-bottom: 10px;
                color: #333333;
                }
                .content p {
                font-size: 16px;
                color: #666666;
                margin-bottom: 20px;
                }
                .footer {
                padding: 10px;
                text-align: center;
                font-size: 12px;
                color: #999999;
                }
            </style>
            </head>
            <body>
            <div class="container">
                <!-- Header with Image -->
                <div class="header">
                <img src="https://www.kapc.or.ke/images/headers/logo.png" alt="Company Logo">
                </div>

                <!-- Main Content -->
                <div class="content">
                <h1>Thank You for Your Submission</h1>
                <p>We are currently in the process of verifying your details. This process may take some time, and we appreciate your patience.</p>
                <p>We will notify you as soon as the verification is complete. In the meantime, if you have any questions, feel free to reach out to us.</p>
                </div>

                <!-- Footer -->
                <div class="footer">
                <p>&copy; 2024 Your Company. All rights reserved.</p>
                <p>Your Company Address, City, Country</p>
                </div>
            </div>
            </body>
            </html>

    """
    print("sen")
    subject, from_email, to = 'Account Details', "info.healthixsolutions@gmail.com",email
    text_content = ''
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_html_email(email):
    sender_email = settings.EMAIL_HOST_USER
    receiver_email = email
    subject = "Test Email with HTML Content"
    smtp_server = settings.EMAIL_HOST_USER  # Example for Gmail
    smtp_port = settings.EMAIL_PORT
    smtp_user = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    # Create a MIMEMultipart object to contain both plain text and HTML content
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Plain-text version of the email content (for clients that can't display HTML)
    plain_text = """\
    Hi,
    This is a test email with plain text content.
    """

    # HTML version of the email content
    html_content = """\
    <html>
      <body>
        <h1>Hello!</h1>
        <p>This is an <b>HTML</b> email.</p>
        <p><a href="https://example.com">Visit our website</a> for more details.</p>
      </body>
    </html>
    """

    # Attach the plain-text and HTML parts to the message
    part1 = MIMEText(plain_text, "plain")
    part2 = MIMEText(html_content, "html")
    message.attach(part1)
    message.attach(part2)

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(smtp_user, smtp_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

# Call the function to send the email


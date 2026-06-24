import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sender's email credentials
sender_email = "rajumm1996@gmail.com"
app_password = "noaqixzdfefxjfod"

# Recipient's email
recipient_email = "rajumm1996@gmail.com"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = "Test Email from Python"
def otp_sender(otp):
			# Add body to email
			body = str(otp)
			message.attach(MIMEText(body, "plain"))

			# Connect to SMTP server (in this case, Gmail's SMTP server)
			server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

			# Login to the email account
			server.login(sender_email, app_password)

			# Send email
			server.sendmail(sender_email, recipient_email, message.as_string())

			# Quit SMTP server
			server.quit()

			print("Email sent successfully to", recipient_email)

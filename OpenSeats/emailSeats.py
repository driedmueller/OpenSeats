import smtplib, ssl

# TODO: Add function from openSeatsGui.py to grab RemainingSeats and save it message variable

port = 465 # for SSL
smtp_server = "smtp.gmail.com"
sender_email = "openseat1909@gmail.com"
receiver_email = "openseat1909@gmail.com"
password = input("Type your password and press enter: ") # not safe practice to store password in code
message = """/
Subject: Hi there

This message is sent from Python."""

# Create a secure SSL context
context = ssl.create_default_context()

# using with makes sure the connection is automatically closed at the end of the indented code block
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
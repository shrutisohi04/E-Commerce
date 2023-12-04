import smtplib

# creates SMTP session
s = smtplib.SMTP("smtp.gmail.com", 587)

# start TLS for security
s.starttls()

# Authentication
s.login("YOUR EMAIL", "")

# message to be sent
message = "Hello"

# sending the mail
s.sendmail("YOUR EMAIL", "SENDER EMAIL", message)

# terminating the session
s.quit()

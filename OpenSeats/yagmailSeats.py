import yagmail

receiver = "driedmueller@atu.edu"
body = "Test to see if yagmail works"

#yag = yagmail.SMTP("openseat1909@gmail.com")
with yagmail.SMTP("openseat1909@gmail.com") as yag:
    yag.send(
        to=receiver,
        subject="Test from yagmail",
        contents=body
        )
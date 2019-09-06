import imaplib
import email
import keyring

email_user = 'openseat1909@gmail.com'
email_password = keyring.get_password('yagmail', 'openseat1909@gmail.com')

mail = imaplib.IMAP4_SSL('imap.gmail.com') #port 993
mail.login(email_user, email_password)
mail.select('Inbox')

type, data = mail.search(None, '(SUBJECT "test")')
mail_ids = data[0]
id_list = mail_ids.split()

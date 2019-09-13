import imaplib, email, keyring, re, csv

email_user = 'openseat1909@gmail.com'
email_password = keyring.get_password('yagmail', 'openseat1909@gmail.com')

try:
    mail = imaplib.IMAP4_SSL('imap.gmail.com') #port 993
    mail.login(email_user, email_password)
    mail.select('Inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    latest_email = ''

    for num in reversed(id_list):
        typ, data = mail.fetch(num, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_from = msg['from']
                if (email_subject.startswith('202020')) or (email_subject.startswith('201980')):
                    sender = re.findall(r'<(.*?)>', email_from)[0] #grabs e-mail address between < and >
                    term, crn = email_subject.split(' ', 1) #subject line splits at the space
                    print(sender)
                    print(email_subject)
                    #add e-mail, term, and crn to csv file
                    with open('input.csv', 'a', newline='') as file:
                        write = csv.writer(file)
                        write.writerow([term, crn, sender])
                            
except Exception as e:
    print(str(e))
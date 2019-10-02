import imaplib, email, keyring, re, csv, requests, yagmail, time
from bs4 import BeautifulSoup

def getSeats(term, crn):
    html = requests.get(f"https://ssbprod.atu.edu/pls/PROD/bwckschd.p_disp_detail_sched?term_in={term}&crn_in={crn}").text

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", attrs={"summary":"This layout table is used to present the seating numbers."})
    if table is None:
        seatsRemaining = "Wrong term/CRN"
    else:
        td_list = table.findAll("td")
        seatsRemaining = td_list[3].text
    table = soup.find("table", attrs={"summary":"This table is used to present the detailed class information."})
    if table is None:
        courseName = "Wrong term/CRN"
        section = "Wrong term/CRN"
    else:
        th_list = table.findAll("th")
        courseInfo = th_list[0].text
        courseName = courseInfo.split("-", 1)[0]
        section = courseInfo.split("-", 4)[3]
    return seatsRemaining, courseName, section

def sendConfirm(term, crn, email, seats, courseName, section):
    year = term[:4]
    if (term[4] == "7"):
        semester = "Fall"
    elif (term[4] == "2"):
        semester = "Spring"
    elif (term[4] == "4"):
        semester = "Summer"
    body = f"""Your request has been received and we will notify you when a seat opens for:
    -----------------------------
    Term:\t{semester} {year}
    CRN:\t{crn}
    Course:\t{courseName}
    Sec: {section}
    Seats:\t{seats}
    -----------------------------
    """

    with yagmail.SMTP("openseat1909@gmail.com") as yag:
        yag.send(
            to=email,
            subject="Confirmation",
            contents=body
            )

def sendOops(term, crn, email):
    body = f"""Oops! Your request contained the wrong Term or CRN.
    One of the following is incorrect:
    -----------------------------
    Term:\t{term}
    CRN:\t{crn}
    -----------------------------
    """

    with yagmail.SMTP("openseat1909@gmail.com") as yag:
        yag.send(
            to=email,
            subject="Wrong Term/CRN",
            contents=body
            )

def sendDup(term, crn, email):
    body = f"""We already have a request on file from you for:
    -----------------------------
    Term:\t{term}
    CRN:\t{crn}
    -----------------------------

    You will be notified of any open seats when they are available.
    """

    with yagmail.SMTP("openseat1909@gmail.com") as yag:
        yag.send(
            to=email,
            subject="Duplicate Request",
            contents=body
            )

email_user = 'openseat1909@gmail.com'
email_password = keyring.get_password('yagmail', 'openseat1909@gmail.com')

def main():   
    mail = imaplib.IMAP4_SSL('imap.gmail.com') # port 993
    mail.login(email_user, email_password)
    mail.select('Inbox')

    type, data = mail.search(None, 'UNSEEN') # UNSEEN only grabs unread e-mails
    mail_ids = data[0]
    id_list = mail_ids.split()
    latest_email = ''

    for num in id_list:
        type, data = mail.fetch(num, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_from = msg['from']
                if (email_subject.startswith('202020')) or (email_subject.startswith('201980')) or (email_subject.startswith('201970')):
                    sender = re.findall(r'<(.*?)>', email_from)[0] # grabs e-mail address between < and >
                    term, crn = email_subject.split(' ', 1) # subject line splits at the space

                    # Save csv file in a list called data
                    with open("input.csv") as file:
                        data = list(csv.reader(file))

                    # add e-mail, term, and crn to csv file
                    with open('input.csv', 'a', newline='') as file:
                        writer = csv.writer(file)

                        # Check csv file to see if requested term, crn, sender is already in file
                        for row in data:
                            if (term == row[0] and crn == row[1] and sender == row[2]):
                                newInfo = False
                                break
                            else:
                                newInfo = True
                        
                        seats, courseName, section = getSeats(term, crn)
                        # if data not already in file add data to csv and email a confirmation
                        if (newInfo):
                            if (seats == "Wrong term/CRN"):
                                print("---Wront term/CRN---")
                                print(sender)
                                print(email_subject)
                                # Send e-mail notifying of wrong term/crn
                                sendOops(term, crn, sender)
                            else:
                                writer.writerow([term, crn, sender])
                                # Possibly send this as debug file
                                print("---New Row Added---")
                                print(sender)
                                print(email_subject)

                                # Send e-mail confirming addition to csv file
                                sendConfirm(term, crn, sender, seats, courseName, section)
                        elif (newInfo == False):
                            # Keep following two lines for debugging; possibly send debug info to another file "debug.csv"
                            print("---Data already in file---")
                            print(sender)
                            print(email_subject)

                            # Send e-mail notifying of duplicate request
                            sendDup(term, crn, sender)

    mail.close()
    mail.logout()

while 1:
    print("\n------Checking------\n")
    main()
    time.sleep(120)
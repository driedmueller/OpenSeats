import imaplib, email, keyring, re, csv, requests, yagmail, time
from bs4 import BeautifulSoup

def getSeats(term, crn):
    html = requests.get(f"https://ssbprod.atu.edu/pls/PROD/bwckschd.p_disp_detail_sched?term_in={term}&crn_in={crn}").text

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", attrs={"summary":"This layout table is used to present the seating numbers."})
    if table is None:
        seatsRemaining = "Invalid term/CRN"
    else:
        td_list = table.findAll("td")
        seatsRemaining = td_list[3].text
    table = soup.find("table", attrs={"summary":"This table is used to present the detailed class information."})
    if table is None:
        courseName = "Invalid term/CRN"
        section = "Invalid term/CRN"
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

    ---------------------------------------
    Course:\t{courseName}
    Sec: {section}
    Seats:\t{seats}
    Term:\t{semester} {year}
    CRN:\t{crn}
    ---------------------------------------
    """

    with yagmail.SMTP("openseat1909@gmail.com") as yag:
        yag.send(
            to=email,
            subject="Confirmation",
            contents=body
            )

def sendOops(term, crn, email):
    body = f"""Oops! Your request contained an invalid Term or CRN.

    One of the following is incorrect:
    -----------------------------
    Term:\t{term}
    CRN:\t{crn}
    -----------------------------

    Please resubmit your request with a valid term or CRN.  Thank you!
    """

    with yagmail.SMTP("openseat1909@gmail.com") as yag:
        yag.send(
            to=email,
            subject="Invalid Term/CRN",
            contents=body
            )

def sendDup(term, crn, email, seats, courseName, section):
    body = f"""We already have a request on file from you for:

    -----------------------------
    Course:\t{courseName}
    Sec: {section}
    Seats:\t{seats}
    Term:\t{term}
    CRN:\t{crn}
    -----------------------------

    You will be notified when a seat is available.  Thank you!
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

                        # If list is empty, go ahead and just write a new row in csv file
                        if not data:
                            writer.writerow([term, crn, sender])
                            # Possibly send this as debug file
                            print("---New Row Added---")
                            print(sender)
                            print(email_subject)
                            seats, courseName, section = getSeats(term, crn)
                            # Send e-mail confirming addition to csv file
                            sendConfirm(term, crn, sender, seats, courseName, section)
                        else:
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
                                # Check if invalid term/crn was requested
                                if (seats == "Invalid term/CRN"):
                                    print("---Invalid term/CRN---")
                                    print(sender)
                                    print(email_subject)
                                    # Send e-mail notifying of Invalid term/crn
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
                                sendDup(term, crn, sender, seats, courseName, section)

    mail.close()
    mail.logout()

def emailSeats():
    # Save csv file in a list called data
    with open("input.csv") as file:
        data = list(csv.reader(file))

    with open("input.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for row in data:
            term = row[0]
            crn = row[1]
            email = row[2]
            seats, courseName, section = getSeats(term, crn)
            if (seats <= "0"):
                #print("\n---Keep---")
                writer.writerow(row)
            elif (seats > "0"):
                sendOpenSeat(term, crn, email, seats, courseName, section)
          
def sendOpenSeat(term, crn, email, seats, courseName, section):
    year = term[:4]
    if (term[4] == "7"):
        semester = "Fall"
    elif (term[4] == "2"):
        semester = "Spring"
    elif (term[4] == "4"):
        semester = "Summer"
    body = f"""The class you requested is currently open:

---------------------------------------
Course:\t{courseName}
Sec: {section}
Seats:\t{seats}
Term:\t{semester} {year}
CRN:\t{crn}
--------------------------------------- 

Your e-mail has been removed from the mailing list.  Thank you!"""

    with yagmail.SMTP("openseat1909@gmail.com") as yag:
        yag.send(
            to=email,
            subject="Open Seat",
            contents=body
            )
    print("\n---Sent open email---")
    print(email, term, crn)

while 1:
    print("\n******Checking Gmail******")
    main()
    print("\n-Wait-")
    time.sleep(120)
    print("\n******Checking CSV******")
    emailSeats()
    print("\n-Wait-")
    time.sleep(120)

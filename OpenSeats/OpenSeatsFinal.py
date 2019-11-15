import imaplib, email, keyring, re, csv, requests, yagmail, time, logging
from bs4 import BeautifulSoup

logging.basicConfig(filename='events.log',level=logging.DEBUG,format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

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

def sendConfirm(term, crn, eAddress, seats, courseName, section):
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
            to=eAddress,
            subject="Confirmation",
            contents=body
            )
    logging.info('---Sent Confirmation---')
    print("---Sent Confirmation---")

def sendOops(term, crn, eAddress):
    body = f"""Oops! Your request contained an invalid CRN.

    The following CRN is incorrect:
    ---------------------------------------
    Term:\t{term}
    CRN:\t{crn}
    ---------------------------------------

    Please resubmit your request with a valid CRN.  Thank you!
    """

    with yagmail.SMTP("openseat1909@gmail.com") as yag:
        yag.send(
            to=eAddress,
            subject="Invalid CRN",
            contents=body
            )
    logging.info('---Sent Invalid CRN---')
    print("---Sent Invalid CRN---")

def sendDup(term, crn, eAddress, seats, courseName, section):
    body = f"""We already have a request on file from you for:

    ---------------------------------------
    Course:\t{courseName}
    Sec: {section}
    Seats:\t{seats}
    Term:\t{term}
    CRN:\t{crn}
    ---------------------------------------

    You will be notified when a seat is available.  Thank you!
    """

    with yagmail.SMTP("openseat1909@gmail.com") as yag:
        yag.send(
            to=eAddress,
            subject="Duplicate Request",
            contents=body
            )
    logging.info('---Sent Duplicate---')
    print("---Sent Duplicate---")

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

                        # If list is empty
                        if not data:
                            seats, courseName, section = getSeats(term, crn)
                            #Get current time for datestamps
                            now = time.time()
                            if (seats == "Invalid term/CRN"):
                                logging.info('---Invalid term/CRN--- SENDER: %s, SUBJECT: %s', sender, email_subject)
                                print("\n---Invalid term/CRN---")
                                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
                                print(sender)
                                print(email_subject)
                                # Send e-mail notifying of Invalid term/crn
                                sendOops(term, crn, sender)
                            elif (seats > "0"):
                                logging.info('---Data Not Added: Class Open--- SENDER: %s, SUBJECT: %s', sender, email_subject)
                                print("\n---Data Not Added: Class Open---")
                                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
                                print(sender)
                                print(email_subject)
                                sendOpenSeat(term, crn, sender, seats, courseName, section)
                            else:
                                writer.writerow([term, crn, sender])
                                # Possibly send this as debug file
                                logging.info('---New Row Added--- SENDER: %s, SUBJECT: %s', sender, email_subject)
                                print("\n---New Row Added---")
                                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
                                print(sender)
                                print(email_subject)
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
                            #Get current time for datestamps
                            now = time.time()
                            # if data not already in file add data to csv and email a confirmation
                            if (newInfo):
                                # Check if invalid term/crn was requested
                                if (seats == "Invalid term/CRN"):
                                    logging.info('---Invalid term/CRN--- SENDER: %s, SUBJECT: %s', sender, email_subject)
                                    print("\n---Invalid term/CRN---")
                                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
                                    print(sender)
                                    print(email_subject)
                                    # Send e-mail notifying of Invalid term/crn
                                    sendOops(term, crn, sender)
                                elif (seats > "0"):
                                    logging.info('---Data Not Added: Class Open--- SENDER: %s, SUBJECT: %s', sender, email_subject)
                                    print("\n---Data Not Added: Class Open---")
                                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
                                    print(sender)
                                    print(email_subject)
                                    sendOpenSeat(term, crn, sender, seats, courseName, section)
                                else:
                                    writer.writerow([term, crn, sender])
                                    # Possibly send this as debug file
                                    logging.info('---New Row Added--- SENDER: %s, SUBJECT: %s', sender, email_subject)
                                    print("\n---New Row Added---")
                                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
                                    print(sender)
                                    print(email_subject)
                                    # Send e-mail confirming addition to csv file
                                    sendConfirm(term, crn, sender, seats, courseName, section)
                            elif (newInfo == False):
                                # Keep following two lines for debugging; possibly send debug info to another file "debug.csv"
                                logging.info('---Data already in file--- SENDER: %s, SUBJECT: %s', sender, email_subject)
                                print("\n---Data already in file---")
                                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
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
            eAddress = row[2]
            seats, courseName, section = getSeats(term, crn)
            if (seats <= "0"):
                #print("\n---Keep---")
                writer.writerow(row)
            elif (seats > "0"):
                sendOpenSeat(term, crn, eAddress, seats, courseName, section)

def sendOpenSeat(term, crn, eAddress, seats, courseName, section):
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
            to=eAddress,
            subject="Open Seat",
            contents=body
            )
    #Get current time for datestamp
    now = time.time()
    logging.info('---Sent open email---')
    print("\n---Sent open email---")
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
    print(eAddress, term, crn)

while 1:
    now = time.time()
    print("\n******Checking Gmail******")
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
    main()
    print("\n-Wait-")
    time.sleep(120)
    now = time.time()
    print("\n******Checking CSV******")
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
    emailSeats()
    print("\n-Wait-")
    time.sleep(120)

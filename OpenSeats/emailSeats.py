# Iterate through csv file. 
# Output remaining seats for classes in csv file.
# Remove row in csv for any open classes.
# Send e-mail to inform of open seat.

import requests, csv, yagmail
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
                print("\n---Keep---")
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

-----------------------------
Term:\t{semester} {year}
CRN:\t{crn}
Course:\t{courseName}
Sec: {section}
Seats:\t{seats}
----------------------------- 

Your e-mail has been removed from the mailing list."""
    print(body)

    #with yagmail.SMTP("openseat1909@gmail.com") as yag:
    #    yag.send(
    #        to=email,
    #        subject="Open Seat",
    #        contents=body
    #        )

emailSeats()
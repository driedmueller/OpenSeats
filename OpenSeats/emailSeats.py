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
    else:
        th_list = table.findAll("th")
        courseInfo = th_list[0].text
        courseName = courseInfo.split("-", 1)[0]
        section = courseInfo.split("-", 4)[3]
    return seatsRemaining, courseName, section

def main():
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
                sendEmail(term, crn, email)
                #print("\n---Email---")

          
def sendEmail(term, crn, email):
    receiver = email
    body = f"""The class you requested is currently open:

-----------------------------
Semester: {term}
CRN: {crn}
----------------------------- """
    print(body)

    #with yagmail.SMTP("openseat1909@gmail.com") as yag:
    #    yag.send(
    #        to=receiver,
    #        subject=f"Open seat in {crn}",
    #        contents=body
    #        )

main()
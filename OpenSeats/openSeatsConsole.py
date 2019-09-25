import requests, csv
from bs4 import BeautifulSoup
import time
import sys

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
    
def readCSV():
    updatedlist = []
    with open("input.csv") as file:
        reader = csv.reader(file)
        #next(reader)
        for row in reader:
            term = row[0]
            year = term[:4]
            if (term[4] == "7"):
                semester = "Fall"
            elif (term[4] == "2"):
                semester = "Spring"
            elif (term[4] == "4"):
                semester = "Summer"
            crn = row[1]
            email = row[2]
            seats, courseName, section = getSeats(term, crn)
            print("\n-----------------------------")
            print(f"Term:\t{semester} {year}")
            print(f"CRN:\t{crn}")
            print(f"Course:\t{courseName}")
            print(f"Sec: {section}")
            print(f"Seats:\t{seats}")
            print("-----------------------------")

readCSV()

#showSeats("201940", "40107", "ENGL 2173-TC1")
#time.sleep(5)
#showSeats("201970", "71832", "MATH 2914-003")
#time.sleep(5)
#showSeats("201970", "71060", "GEOG 2013-M02")
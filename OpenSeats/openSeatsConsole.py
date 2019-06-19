import requests
from bs4 import BeautifulSoup
import time
import sys

def showSeats(term, crn, course):

    html = requests.get(f"https://ssbprod.atu.edu/pls/PROD/bwckschd.p_disp_detail_sched?term_in={term}&crn_in={crn}").text

    """html=
	    <table class="datadisplaytable" summary="This layout table is used to present the seating numbers." width="100%">
		    <caption class="captiontext">Registration Availability</caption>
		    <tbody>
			    <tr>
				    <td class="dddead">&nbsp;</td>
				    <th class="ddheader" scope="col"><span class="fieldlabeltext">Capacity</span></th>
				    <th class="ddheader" scope="col"><span class="fieldlabeltext">Actual</span></th>
				    <th class="ddheader" scope="col"><span class="fieldlabeltext">Remaining</span></th>
			    </tr>
			    <tr>
				    <th class="ddlabel" scope="row" style="background: none; color: rgb(0, 0, 0);"><span class="fieldlabeltext">Seats</span></th>
				    <td class="dddefault">20</td>
				    <td class="dddefault">15</td>
				    <td class="dddefault">5</td>
			    </tr>
		    </tbody>
	    </table>
	    """

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", attrs={"summary":"This layout table is used to present the seating numbers."})
    td_list = table.findAll("td")
    seatsRemaining = td_list[3].text
    print("\n-----------------------------")
    print(f"Semester: {term}")
    print(f"Course: {course}")
    print(f"Open Seats: {seatsRemaining}")
    print("-----------------------------")

"""
try:
    while True:
        showSeats("201970", "71832", "MATH 2914-003")
        time.sleep(5)
except KeyboardInterrupt:
    print("Quitting the program")
except:
    print("Unknown error occurred")
"""

showSeats("201940", "40107", "ENGL 2173-TC1")
time.sleep(5)
showSeats("201970", "71832", "MATH 2914-003")
time.sleep(5)
showSeats("201970", "71060", "GEOG 2013-M02")
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk


def getSeats(*args):
	term = semester.get()
	crn = course.get()

	#html = requests.get(f"https://ssbprod.atu.edu/pls/PROD/bwckschd.p_disp_detail_sched?term_in={term}&crn_in={crn}").text

	html="""
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
					<td class="dddefault">20</td>
					<td class="dddefault">0</td>
				</tr>
			</tbody>
		</table>
		"""

	soup = BeautifulSoup(html, "html.parser")
	table = soup.find("table", attrs={"summary":"This layout table is used to present the seating numbers."})
	td_list = table.findAll("td")
	seatsRemaining = td_list[3].text
	seats.set(seatsRemaining)


root = Tk()
root.title("Remaining Seats")

mainframe = ttk.Frame(root, padding="20 20")
mainframe.grid(column=0, row=0)

semester = StringVar()
course = StringVar()
seats = StringVar()

ttk.Label(mainframe, text="Enter Term:").grid(row=1, column=1)
ttk.Label(mainframe, text="Enter CRN:").grid(row=2, column=1)
semesterEntry = ttk.Entry(mainframe, textvariable=semester).grid(row=1, column=2)
courseEntry = ttk.Entry(mainframe, textvariable=course).grid(row=2, column=2)
ttk.Label(mainframe, text="Remaining Seats:").grid(row=3, column=1)
ttk.Label(mainframe, textvariable=seats).grid(row=3, column=2)
ttk.Button(mainframe, text="Show me the seats!", command=getSeats).grid(row=4, column=2)

root.mainloop()
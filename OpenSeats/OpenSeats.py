import requests
from bs4 import BeautifulSoup

term = input("Enter term: ")
crn = input("Enter crn: ")

html = requests.get(f"https://ssbprod.atu.edu/pls/PROD/bwckschd.p_disp_detail_sched?term_in={term}&crn_in={crn}").text

"""html =
    <table class="datadisplaytable" summary="This layout table is used to present the seating numbers." width="100%">
        <caption class="captiontext">Registration Availability</caption>
        <tbody>
            <tr>
                <td class="dddead">&nbsp;</td>
                <th class="ddheader" scope="col">
                    <span class="fieldlabeltext">Capacity</span>
                </th>
                <th class="ddheader" scope="col">
                    <span class="fieldlabeltext">Actual</span>
                </th>
                <th class="ddheader" scope="col">
                    <span class="fieldlabeltext">Remaining</span>
                </th>
            </tr>
            <tr>
                <th class="ddlabel" scope="row" style="background: none; color: rgb(0, 0, 0);">
                    <span class="fieldlabeltext">Seats</span>
                </th>
                <td class="dddefault">30</td>
                <td class="dddefault">30</td>
                <td class="dddefault">0</td>
            </tr>
        </tbody>
    </table>"""

soup = BeautifulSoup(html, "html.parser")
table = soup.find("table", attrs={"summary":"This layout table is used to present the seating numbers."})
td_list = table.findAll("td")
seatsRemaining = td_list[3].text
print(seatsRemaining)

from selenium import webdriver
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox(executable_path=r'C:\Program Files\Python\geckodriver.exe')
driver.get('https://ssbprod.atu.edu/pls/PROD/bwckschd.p_disp_dyn_sched')

select = Select(driver.find_element_by_id(''))

# select by visible text
# select.select_by_visible_text('Banana')

# select by value 
select.select_by_value('202020')
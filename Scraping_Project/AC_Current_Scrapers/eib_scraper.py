from builtins import str
from builtins import range
from builtins import object
from datetime import datetime

import time
import datetime
import unicodecsv
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def scrape():
    with open('eib_scraped.csv', 'wb') as file:
        writer = unicodecsv.writer(file)
        header = [
            'IAM',
            'Year',
            'Country',
            'Project',
            'ID',
            'IAM ID',
            'Filer(s)',
            'Environmental Category',
            'Project Company',
            'Project Number',
            'Related Project Number',
            'Project Type',
            'Financial Institution',
            'Project Loan Amount',
            'Sector',
            'Issues',
            'Complaint Status',
            'Filing Date',
            'Registration Start Date',
            'Registration End Date',
            'Eligibility Start Date',
            'Eligibility End Date',
            'Dispute Resolution Start Date',
            'Dispute Resolution End Date',
            'Compliance Review Start Date',
            'Compliance Review End Date',
            'Monitoring Start Date',
            'Monitoring End Date',
            'Compliance Report Issued?',
            'Date Closed',
            'Documents',
            'Hyperlink',
            'Project Date',
            'Project Status',
            'Project Description',
        ]
        writer.writerow(header)
        driver = webdriver.Chrome()
        eib_scrape(driver, writer)
        time.sleep(2)
        driver.quit()

def eib_scrape(driver, writer):
    driver.get('http://www.eib.org/about/accountability/complaints/cases/index.htm')
    main_window = driver.current_window_handle
    time.sleep(2)
    select_all = driver.find_element_by_xpath('//*[@id="consultationsList"]/div/div[3]/div[1]/select/option[4]')
    select_all.click()
    time.sleep(2)
    # button = driver.find_element_by_xpath('//*[@id="helpUsWebsite"]/div/div[2]/a[1]').click()
    time.sleep(1)
    button = driver.find_element_by_xpath('//*[@id="footer"]/div[3]/div[2]/div/p/button').click()
    time.sleep(1)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(1)
    rows = driver.find_elements_by_xpath('//*[@id="consultationsList"]/div/table/tbody/tr')
    row_range = range(1, len(rows)+1)
    for row in row_range:
        case_type = driver.find_element_by_xpath('//*[@id="consultationsList"]/div/table/tbody/tr[%s]/td[2]' % row).text
        if case_type == 'E':
            filing_date = driver.find_element_by_xpath('//*[@id="consultationsList"]/div/table/tbody/tr[%s]/td[1]' % row).text
            complaint_status = driver.find_element_by_xpath('//*[@id="consultationsList"]/div/table/tbody/tr[%s]/td[7]' % row).text
            project_link = driver.find_element_by_xpath('//*[@id="consultationsList"]/div/table/tbody/tr[%s]/td[3]/a' % row)
            project = project_link.text
            country = driver.find_element_by_xpath('//*[@id="consultationsList"]/div/table/tbody/tr[%s]/td[4]' % row).text
            year = filing_date[-4:]
            project_link.click()
            # iframe = driver.find_element_by_tag_name('noscript')
            # iframe1 = driver.find_element_by_tag_name('iframe')
            # driver.switch_to.frame()
            driver.switch_to_window(driver.window_handles[1])
            driver.switch_to.default_content()
            try:
                case_text = driver.find_element_by_xpath('//*[@id="consultations"]').text
                junk, case_text = case_text.split('Reference: ', 1)
                case_id, junk = case_text.split('\n', 1)
                try: 
                    junk, case_text = case_text.strip().split('Complainant: ', 1)
                    filer, junk = case_text.split('\n', 1)
                except ValueError:
                    print('Error')
            except Exception as error:
                case_id = None
                filer = None
            registration_start_date = filing_date
            stages = driver.find_elements_by_class_name('caseDate')
            # for stage in stages:
                # print(stage.text)
            # registration_end_date = driver.find_element_by_xpath('//*[@id="consultations"]/div[1]/div[1]/div[2]').text
            # eligibility_start_date = registration_end_date
            # eligibility_end_date = driver.find_element_by_xpath('//*[@id="consultations"]/div[1]/div[2]/div[2]').text
            # cr_start_date = driver.find_element_by_xpath('//*[@id="consultations"]/div[1]/div[3]/div[2]').text
            # dr_end_date = driver.find_element_by_xpath('//*[@id="consultations"]/div[1]/div[4]/div[2]').text
            # cr_end_date = driver.find_element_by_xpath('//*[@id="consultations"]/div[1]/div[5]/div[2]').text
            # date_closed = driver.find_element_by_xpath('//*[@id="consultations"]/div[1]/div[6]/div[2]').text
            # try:
            #     monitoring_end_date = driver.find_element_by_xpath('//*[@id="consultations"]/div[1]/div[7]/div[2]').text
            # except NoSuchElementException:
            #     print('Monitoring: %s' %error)
            #     monitoring_end_date = None
            row_data = [
                'EIB',
                year,
                country,
                project,
                case_id,
                29,
                filer,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                complaint_status,
                filing_date,
                registration_start_date,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                driver.current_url,
                None,
                None,
                None,
            ]
            writer.writerow(row_data)
            print(row_data)
            driver.close()
            driver.switch_to_window(main_window)
            # driver.execute_script('window.history.go(-1)')
            time.sleep(0.7)
            # select_all = driver.find_element_by_xpath('//*[@id="consultationsList"]/div/div[3]/div[1]/select/option[5]')
            # select_all.click()
            time.sleep(2)
            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
            time.sleep(1)
            scroll_modifier = int(row) * 40
            driver.execute_script("window.scrollTo(0, %s)" % scroll_modifier) 
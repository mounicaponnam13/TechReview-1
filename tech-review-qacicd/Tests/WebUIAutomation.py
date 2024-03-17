import csv
import os
import time
import re
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ContextStorage import contextStorage
import unittest
from selenium.webdriver.common.by import By

class webuitest(unittest.TestCase):
    # Define test methods starting with the word "test"
    contextStorage = contextStorage()

    def Is_it_date(self, date_str):
        # Regular expression to match 'DD-MM-YYYY' format
        regex_pattern = r'^(\d{4})-(\d{2})-(\d{2})$'
        regex_pattern_1 = r'^(\d{2})-(\d{2})-(\d{4})$'

        # Check if the string matches the regex pattern
        match = re.match(regex_pattern, date_str)
        match1 = re.match(regex_pattern_1,date_str)

        if match or match1:
            # Extract day, month, and year
            # year, month, day = match.groups()
            #
            # # Change format to 'DD/MM/YYYY'
            # new_date_format = f'{month}/{day}/{year}'
            return True
        else:
            return False

    def Is_it_number(self, data):
        pattern = r'^[-+]?[0-9]*\.?[0-9]+$'
        return bool(re.match(pattern, data))

    def format_number(self, number):
        return float(number)

    def format_date(self,date):
        regex_pattern = r'^(\d{4})-(\d{2})-(\d{2})$'
        regex_pattern_1 = r'^(\d{2})/(\d{2})/(\d{4})$'

        # Check if the string matches the regex pattern
        match = re.match(regex_pattern, date)
        match1 = re.match(regex_pattern_1, date)

        if match:
            # Extract day, month, and year
            year, month, day = match.groups()
            #
            # # Change format to 'DD/MM/YYYY'
            new_date_format = f'{month}/{day}/{year}'
            return new_date_format
        elif match1:
            month, day, year = match1.groups()
            #
            # # Change format to 'DD/MM/YYYY'
            new_date_format = f'{month}/{day}/{year}'
            return new_date_format

    def compare_csv_lists(self, actual_list, expected_list):
        if len(actual_list) != len(expected_list):
            print('lengths of -1')
            return False  # If lengths are different, lists are not equal

        for i in range(len(actual_list)):
            print('lengths of -2')
            if len(actual_list[i]) != len(expected_list[i]):
                print('lengths of -3')
                return False  # If lengths of rows are different, rows are not equal

            for j in range(len(actual_list[i])):
                # print(f'actual - {self.change_date_format(actual_list[i][j])}   expected  {expected_list[i][j]}')
                # actual = self.change_date_format(actual_list[i][j])
                # expected = expected_list[i][j]
                # if  (expected_list[i][j] != self.change_date_format(actual_list[i][j])) or   not in ():
                #     print(f'actual - {self.change_date_format(actual_list[i][j])}   expected  {expected_list[i][j]}')
                #     print('lengths of -12')
                #     print(type(actual_list[i][j]))
                #     return False  # If any element is different, rows are not equal
                if self.Is_it_date(actual_list[i][j]):
                    date1=self.format_date(actual_list[i][j])
                    date2=self.format_date(expected_list[i][j])
                    if date1 != date2:
                        return False
                elif self.Is_it_number(actual_list[i][j]):
                    data1 = self.format_number(actual_list[i][j])
                    data2 = self.format_number(expected_list[i][j])
                    if data1 != data2:
                        return False
                else:
                    if actual_list[i][j] != expected_list[i][j]:
                        return False
        return True

    def read_csv(self, filename):
        rows = []
        with open(filename, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows.append(row)
        return rows

    def test_web_app_features(self):
        page_load_timeout = 10
        project_dir = os.getcwd()
        chromedriver_path = os.path.join(os.path.dirname(project_dir), 'code', 'Driver', 'chromedriver.exe')
        print(chromedriver_path+"-------")
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service)
        driver.set_page_load_timeout(page_load_timeout)
        driver.get("http://localhost:8000/")
        WebDriverWait(driver, page_load_timeout).until(EC.title_is("Arva Test App"))
        page_title = driver.title
        url_loaded = driver.current_url
        assert page_title == "Arva Test App", 'application title name is not as expected'
        assert url_loaded == 'http://localhost:8000/', 'the current url is not as expected'
        login_button=WebDriverWait(driver, page_load_timeout).until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Log In']")))
        login_button.click()
        # perform login
        username_input = WebDriverWait(driver, page_load_timeout).until(
            EC.visibility_of_element_located((By.ID, "id_username")))
        username_input.send_keys('testadmin')
        password_input = WebDriverWait(driver, page_load_timeout).until(
            EC.visibility_of_element_located((By.ID, "id_password")))
        password_input.send_keys('pass1234')
        login_button = WebDriverWait(driver, page_load_timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//button[text()='Log In']")))
        login_button.click()
        upload_data_file = WebDriverWait(driver, page_load_timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//a[text()='Upload Data File']")))
        upload_data_file.click()
        file_path = os.path.join(os.path.dirname(project_dir), 'Data', 'sample.csv')
        choose_file_button = WebDriverWait(driver, page_load_timeout).until(
            EC.visibility_of_element_located((By.ID, "fileupload")))
        choose_file_button.send_keys(file_path)
        submit_button = WebDriverWait(driver, page_load_timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@value = 'Submit']")))
        submit_button.click()
        time.sleep(5)

        driver.get("http://localhost:8000/sampledataview/")
        WebDriverWait(driver, page_load_timeout).until(EC.title_is("Arva Test App"))
        time.sleep(5)
        rows = self.read_csv(file_path)
        actual_data=[]
        all_rows = driver.find_elements(By.XPATH,"//table//tbody//tr")
        for i in range(1,len(all_rows)+1):
            all_cols = driver.find_elements(By.XPATH,f"//table//tbody//tr[{i}]//td")
            data= []
            elem_tracker = 1
            for elem in all_cols:
                if elem_tracker !=1:
                    data.append(elem.text)
                elem_tracker += 1
            actual_data.append(data)
        assert self.compare_csv_lists(rows[1:len(actual_data)+1], actual_data) == True, 'data uploaded from excel is not same on application'

        # Navigate to Map

        driver.get("http://localhost:8000/")
        WebDriverWait(driver, page_load_timeout).until(EC.title_is("Arva Test App"))
        time.sleep(5)
        map_link = WebDriverWait(driver, page_load_timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//a[text()='Map']")))
        map_link.click()
        zoom_button = WebDriverWait(driver, page_load_timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@title='Zoom in']")))
        zoom_button.click()
        zoom_button.click()
        zoom_button.click()
        driver.quit()

# This block allows the test script to be executed directly
if __name__ == '__main__':
    unittest.main()


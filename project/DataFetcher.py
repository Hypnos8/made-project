import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
from selenium.webdriver.chrome.options import Options

from exceptions import FetchingException

class DataFetcher():
    def __init__(self):
        self.temp_dir =  os.getcwd() + "\\tmp\\"
        self.target_dir = os.getcwd() + "\\downloaded_data\\"
        self.driver = self.__configure_webdriver()

    def fetch_data(self, url, expected_filename):
        """Download Data from data.lacity.org 

        Parameters:

        url(string): URL of the "About" Page of the dataset
        expected_filename (string): Filename of the newly downloaded file

        Returns:
        string:Path to downloaded file
        """
        self.clear_temp_dir()
        self.driver.get(url)
        self.driver.implicitly_wait(3)
        
        export_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="export-data-button"]')
        export_button.click()
        download_button = self.driver.find_element(By.CSS_SELECTOR, value='[data-testid="export-download-button"]')
        download_button.click()

        successful_download = False

        # Download is finished if the corresponding CSV was downloaded to the temp dir 
        for i  in range(1000):
            nr_csv_files = len([x for x in os.listdir(self.temp_dir) if x.endswith(".csv")])
            if nr_csv_files > 0 :
                successful_download = True
                print("successfully downloaded ")
                break
            sleep(1)
        if not successful_download:
            raise FetchingException(url)
    
        Path(self.target_dir).mkdir(exist_ok=True)

        file_path_new = self.target_dir + expected_filename
        file_path_old = self.temp_dir + os.listdir(self.temp_dir)[0]
        os.rename(file_path_old, file_path_new)
        return file_path_new

    def __configure_webdriver(self):
        """
        Configure selenium webdriver
        """
        options_chrome = Options()

        # Set download path
        print(self.temp_dir)
        Path(self.temp_dir).mkdir(exist_ok=True)

        options_chrome.add_experimental_option("prefs", {
            "download.default_directory"  : self.temp_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade"  : True,
    })
        # Create driver
        driver = webdriver.Chrome(options=options_chrome)
        return driver
                
    def cleanup(self):
        """
        Stop Selenium when tasks are done
        """
        self.driver.quit()

    def clear_temp_dir(self):
        """
        Remove all files in temp dir
        """
        for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))

import os
import urllib.error
import zipfile
from time import sleep
from urllib.request import urlretrieve

from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
from selenium.webdriver.chrome.options import Options
import retry
from exceptions import FetchingException


class DataFetcher:
    def __init__(self, working_dir):
        self.temp_dir = os.path.join(working_dir, "tmp")
        self.target_dir = os.path.join(working_dir, "downloaded_data")
        Path(self.target_dir).mkdir(exist_ok=True, parents=True)

        self.driver = self.__configure_webdriver()

    @retry.retry(FetchingException, tries=3, delay=2)  # Retries are logged automatically if logging is enabled
    def fetch_data_la_city(self, url, expected_filename, download_timeout_seconds):
        """Download Data from data.lacity.org 

        Parameters:

        url(string): URL of the "About" Page of the dataset
        expected_filename (string): Filename of the newly downloaded file

        Returns:
        string:Path to downloaded file
        """
        self.__clear_temp_dir()
        self.driver.get(url)
        self.driver.implicitly_wait(3)

        export_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="export-data-button"]')
        export_button.click()
        download_button = self.driver.find_element(By.CSS_SELECTOR, value='[data-testid="export-download-button"]')
        download_button.click()
        self.__wait_for_download("csv", url, download_timeout_seconds)

        file_path_new = self.__move_file(expected_filename)
        return file_path_new

    @retry.retry(urllib.error.HTTPError, tries=3, delay=2)
    def fetch_kaggle_geodata(self, url, expected_shp_filename):
        """Download Data from kaggle (via direct download)

        Parameters:

        url(string): URL to the dataset
        expected_shp_filename (string): expected Filename of .shp file that we will use

        Returns:
        string:Path to downloaded file
        """
        self.__clear_temp_dir()
        zipfile_location = os.path.join(self.temp_dir, "archive.zip")
        urlretrieve(url, zipfile_location)
        with zipfile.ZipFile(zipfile_location, 'r') as myzip:
            myzip.extractall(self.temp_dir)
        os.remove(zipfile_location)
        for f in os.listdir(self.temp_dir):
            os.rename(os.path.join(self.temp_dir,  f), os.path.join(self.target_dir, f))

        self.__clear_temp_dir()

        return os.path.join(self.target_dir, expected_shp_filename)

    @retry.retry(urllib.error.HTTPError, tries=3, delay=2)
    def fetch_population_data(self, url, expected_shp_filename):
        """Download Data from kaggle (via direct download)

        Parameters:

        url(string): URL to the dataset
        expected_shp_filename (string): expected Filename of .shp file that we will use

        Returns:
        string:Path to downloaded file
        """
        self.__clear_temp_dir()
        file_name = os.path.join(self.temp_dir, "population.json")
        urlretrieve(url, file_name)
        os.rename(os.path.join(self.temp_dir,  file_name), os.path.join(self.target_dir, file_name))

        self.__clear_temp_dir()

        return os.path.join(self.target_dir, expected_shp_filename)


    def __wait_for_download(self, filetype, url, download_timeout_seconds):
        """
        Wait for download of file
        required as there's no event fired by selenium when a download is finished
        """
        # Download is finished if the corresponding CSV was downloaded to the temp dir
        successful_download = False
        for i in range(download_timeout_seconds):
            nr_csv_files = len([x for x in os.listdir(self.temp_dir) if x.endswith("." + filetype)])
            if nr_csv_files > 0:
                successful_download = True
                print("successfully downloaded file from " + url)
                break
            sleep(1)
        if not successful_download:
            raise FetchingException(url)

    def __move_file(self, expected_filename):
        Path(self.target_dir).mkdir(exist_ok=True)

        file_path_new = os.path.join(self.target_dir, expected_filename)
        file_path_old = os.path.join(self.temp_dir, os.listdir(self.temp_dir)[0])
        os.rename(file_path_old, file_path_new)
        return file_path_new

    def __configure_webdriver(self):
        """
        Configure selenium webdriver
        """
        options_chrome = Options()

        # Set download path
        print(self.temp_dir)
        Path(self.temp_dir).mkdir(exist_ok=True, parents=True)

        options_chrome.add_experimental_option("prefs", {
            "download.default_directory": self.temp_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            'intl.accept_languages': 'en,en_US'
        })
        # Create driver
        driver = webdriver.Chrome(options=options_chrome)
        return driver

    def cleanup(self):
        """
        Stop Selenium when tasks are done
        """
        self.driver.quit()

    def __clear_temp_dir(self):
        """
        Remove all files in temp dir
        """
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))

from bs4 import BeautifulSoup
import requests
from AppTorrent import AppTorrent
from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
import json
from os import path

class TorrentDownloader:
    def __init__(self, webdriver_path, download_path, already_downloaded_path, url):
        self.url = url
        self.download_path = download_path
        self.webdriver_path = webdriver_path
        self.already_downloaded_path = already_downloaded_path
        self.already_downloaded = self.get_already_downloaded(already_downloaded_path)
        self.__check_settings()

    def get_already_downloaded(self, path):
        return json.load(open(path, "r"))["downloaded"]
    
    def create_json_file(self):
        json.dump({"downloaded":[]}, open(self.already_downloaded_path, "w+"))
    
    def __check_settings(self):
        if not path.isdir(self.download_path):
            raise FileNotFoundError(f"{self.download_path} doesn't exist")

        if not path.isfile(self.webdriver_path):
            raise FileNotFoundError(f"chrome driver not found at {self.webdriver_path}")
        
        if not path.isfile(self.already_downloaded_path):
            raise FileNotFoundError(f"{self.already_downloaded_path} file doesn't exist")

    
    def __setup_chromedriver(self):
        os.path.isdir(self.download_path)
        os.environ["webdriver.chrome.driver"] = self.webdriver_path
        
        chrome_options = Options()
        prefs = {
            'profile.default_content_setting_values.automatic_downloads': 1,
            "download.prompt_for_download":False,
            "download.default_directory":self.download_path}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--headless")  
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def __fetch_new_torrents(self):
        torrents = list()
        soup = BeautifulSoup(requests.get(self.url).text, features="lxml")
        links  = list(map(lambda x: x["href"], soup.find_all("a", {"class": "download"})))
        names = list(map(lambda x: x.find("a")["title"],soup.find_all("h3", {"class": "entry-title"})))

        for i in range(0,len(links)):
            if links[i] not in self.already_downloaded:
                torrents.append(AppTorrent(names[i], links[i]))
        return torrents

    def __add_to_downloaded(self, liste_downloaded):
        file = open(self.already_downloaded_path, "w")
        if len(self.already_downloaded) > 1000:
            json.dump({"downloaded":liste_downloaded}, file)
        else:
            self.already_downloaded.extend(liste_downloaded)
            json.dump({"downloaded":self.already_downloaded}, file)
        
    def download_torrents(self):

        downloaded = list()
        fetched_torrents = self.__fetch_new_torrents()
        driver = self.__setup_chromedriver()
        for torrent in fetched_torrents:
            print(f"[+] downloading {torrent.app_name}")
            driver.get(torrent.url)
            downloaded.append(torrent.url)

        self.__add_to_downloaded(downloaded)
        print("download finished")

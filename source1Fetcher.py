from bs4 import BeautifulSoup
import requests
from AppTorrent import AppTorrent
import sys
from concurrent.futures import ThreadPoolExecutor


class source1Fetcher:
    def __init__(self, already_downloaded):
        self.already_downloaded = already_downloaded
    
    def get_first_links(self):
        url = "https://torrentmac.net"
        request =  requests.get(url)
        if 200 <= request.status_code < 300:
            soup = BeautifulSoup(request.text, "lxml")
            return map(lambda x: x["href"],soup.find_all("a", {"class": "home-thumb"} , href=True))
        else:
            print(f"[-] couldn't connect to {url}")
            sys.exit()
    
    def get_torrent_link_on_page(self, link):
        page = BeautifulSoup(requests.get(link).text, "lxml")
        url = page.find("a", {"class":"download-btn"}, href=True)["href"]
        
        name = page.find("h1", {"class":"post-title"}).text
        return AppTorrent(name, url)
        
    def get_every_link_threaded(self):
        torrents = set()
        links = self.get_first_links()
        pool = ThreadPoolExecutor(max_workers=20)
        for torrent in pool.map(self.get_torrent_link_on_page, links):
            if torrent.url not in self.already_downloaded:
                torrents.add(torrent)
        return torrents

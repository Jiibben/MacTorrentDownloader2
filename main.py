from TorrentDownloader_2 import TorrentDownloader
from ConfigHandler import ConfigHandler

CONFIG_PATH = "./config.json"
if __name__ == "__main__":
    try:    
        config = ConfigHandler(CONFIG_PATH)
        downloader = TorrentDownloader(config.webdriver_path, config.download_path, config.already_downloaded_json)
        downloader.download_torrents()
    except:
        print("[-] exiting program")
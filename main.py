from TorrentDownloader import TorrentDownloader
from ConfigHandler import ConfigHandler

CONFIG_PATH = "./config.json"
if __name__ == "__main__":
    
    config = ConfigHandler(CONFIG_PATH)
    downloader = TorrentDownloader(config.webdriver_path, config.download_path, config.already_downloaded_path, config.url)
    downloader.download_torrents()

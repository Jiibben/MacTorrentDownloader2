import json
import os
import sys
import pyfiglet
import subprocess

def create_json_file():
    print("[+] creating already downloaded file in current working dir")
    json.dump({"downloaded":[]}, open("already_downloaded.json", "w+"))

def get_download_path():
    path = input("Enter absolute path to where torrents will be downloaded :")
    if os.path.isdir(path) and os.path.isabs(path):
        print("[+] successfully found download folder")
    else:
        print("[-] download path doesn't exist")
        print(f"[+] creating download folder : {path}")
        os.system(f"mkdir -p {path}")
    return path

def webdriver_path():
    path = input(f"Enter chromedrive path it's likely : ")
    if os.path.isfile(path):
        print("[+] successfully found chromedriver")
    else:
        print("[-] didn't find chromedriver exiting ...")
        sys.exit()
    return path


def config_file():
    print("[+] creating config file in current working dir")
    json.dump({
    "webdriver_path":f"{webdriver_path()}",
    "download_path":f"{get_download_path()}",
    "already_downloaded_json":f"{os.getcwd()}/already_downloaded.json",
    "url":"https://mac-torrents.io/"
}, open("config.json", "w+"))


def getting_required_pip():
    with open(os.devnull, 'wb') as devnull:
        subprocess.check_call(['pip3', 'install', "-r", "requirements.txt"], stdout=devnull, stderr=subprocess.STDOUT)
    print("[+] successfully installed requirements")

if __name__ == "__main__":
    print("installing dependencies")
    getting_required_pip()
    print(pyfiglet.figlet_format("TORRENT DOWNLOADER"))
    print(" made by Jibben ".center(65, "-"))
    print("")
    print("make sure that you have google chrome installed and the latest chromedriver (and you know the path to it)")
    print("")
    create_json_file()
    config_file()

    
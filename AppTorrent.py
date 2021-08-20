class AppTorrent:
    def __init__(self, app_name, url):
        self.app_name = app_name
        self.url = url        

    def __repr__(self):
        return self.app_name
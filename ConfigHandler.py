import json
class ConfigHandler:
    def __init__(self, config_path):
        self.config_path = config_path
        self.__fetch_config()

    
    def __read_config(self):
        return json.load(open(self.config_path, "r"))
    
    def __fetch_config(self):
        config = self.__read_config()
        for i in config:
            setattr(self, i, config[i])


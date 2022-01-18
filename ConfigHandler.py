import json
class ConfigHandler:
    def __init__(self, config_path):
        self.config_path = config_path
        self.__fetch_config()

    
    def __read_config(self):
        try:
            a = json.load(open(self.config_path, "r"))
        except FileNotFoundError:
            print("[-] config file not found please run the setup.py")

    def __fetch_config(self):
        config = self.__read_config()
        for i in config:
            setattr(self, i, config[i])

    def __set_config(self, conf_obj):
        json.dump(open(self.config_path, "w+"), conf_obj)

    def add_config(self, name, arg):
        conf = self.__read_config()
        conf[name] = arg
        self.__set_config()
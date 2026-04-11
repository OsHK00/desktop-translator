import json

class Config:
    def __init__(self, config_file: str):

        with open(config_file, mode="r", encoding="utf-8") as f:
            self.config = json.load(f)

    def get_default(self):
        data = self.config["default"]
        if data == None:
            return "No data"
        else:
            return data
    
    def get_languages(self):
        return self.config["languages"]
    
    def get_default_to(self):
        return self.get_default()["to"]
    
    def get_default_from(self):
        return self.get_default()["from"] 
    
    def get_favorites(self):
        return self.config["favorites"]

    def set_default_to(self, to_):
        self.config["default"]["to"] = to_
        with open("config.json", mode="w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
    def set_default_from(self, from_):
        self.config["default"]["from"] = from_
        with open("config.json", mode="w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
    def swap_default(self):
        pre_from = self.get_default_from()
        pre_to = self.get_default_to()

        self.config["default"]["from"] = pre_to
        self.config["default"]["to"] = pre_from

        with open("config.json", mode="w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)


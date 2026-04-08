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
    
    def get_deafult_to_(self):
        return self.get_default()["to"]
    
    def get_default_from(self):
        return self.get_default()["from"]
    
configuracion = Config("config.json")
print("defatul: ",configuracion.get_default())

print("languajes: ",configuracion.get_languages())

print("default_to: ", configuracion.get_deafult_to_())
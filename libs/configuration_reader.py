import json 

class ConfigurationReader():

    fileName = "configuration.json"

    @classmethod
    def read_config_file(cls,absolute_path="./"):
        with open(f"{absolute_path}{cls.fileName}", "r") as jsonfile:
            data = json.load(jsonfile)
            jsonfile.close()
        return data
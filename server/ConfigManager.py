#!/env/bin/python
# encoding: utf-8

import json

class ConfigManager:
    def __init__(self):
        self.config_file = "./mmrzConfig.json"

    def read_config_file(self):
        content_dict = {}

        with open (self.config_file) as fr:
            content_json = fr.read()
            content_dict = json.loads(content_json)

        return content_dict

if __name__ == '__main__':
    configMgr = ConfigManager()
    config = configMgr.read_config_file()



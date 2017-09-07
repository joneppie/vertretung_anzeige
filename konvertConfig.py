import configparser

class ConfigLeser:
    def __init__(self, bereich):
        self.bereich = bereich
        self.config = configparser.ConfigParser()
        self.config.read('config.txt')
        if bereich not in self.config.sections():
            raise Exception('Bereich: "' + bereich +
                            '" ist nicht in der Config vorhanden')

    def getWert(self, key, defaultWert = None):
        return self.config[self.bereich].get(key, defaultWert)

    def getPflichtWert(self, key):
        value = self.config[self.bereich].get(key)
        if value == None or value == "":
            raise Exception('Pflichtwert "' + key +
                            '" im Bereich "' + self.bereich +
                            '" ist nicht in der Config vorhanden')
        return value

if __name__ == "__main__":
    print("Klasse ist nicht direkt aufrufbar")

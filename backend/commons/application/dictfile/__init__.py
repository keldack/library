        
class DictFile():
    """
    Memory Repository is just a domain entity object storage like a DB memory. It is instantiated as singleton
    """
   
    def __init__(self, filename, key):

        self._container = {}
        self._filename = filename
        self._key = key
        self.__load_file()


    def __load_file(self):
        """
        Load user from file save
        """
        self._container = {}
        with open(self._filename, "r") as file:
            for line in file.readlines():
                dico = {}
                for item in line.split("//"):
                    detail = item.split(":")
                    dico[detail[0]] = detail[1]
                self._container[dico[self._key]] = dico


    def __save_file(self):
        """
        Save user DB on drive
        """
        with open(self._filename, "w") as file:
            for entry in self._container.values():
                txt = "//".join([f"{key}:{value}" for key, value in entry.items()])
                file.write(txt + "\n")
        print("DictFile: file saved !")


    def add_entry(self, entry):
        self._container[entry[self._key]] = entry
        self.__save_file()

    @property
    def container(self):
        return self._container
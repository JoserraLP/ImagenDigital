import json

class JsonLoader:
    """Loads json file as dict"""

    @staticmethod
    def load(path: str):
        """Loads a json file as dictionary (dict)

        Args:
            path (str): The path where the asc file can be found

        Returns:
            dict: Dictionary that contains the json data
        """

        with open(path) as file:
            data = json.loads('\n'.join(file.readlines()))
            file.close()
            return data


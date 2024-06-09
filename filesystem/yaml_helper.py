import yaml

class YamlHelper():
    '''
    To handle read/write yaml file
    '''

    def read_yaml(file_path):
        '''
        Read data from the yaml file.

        :param str file_path: Path of the yaml file.
        :return dict: The data from the yaml file.
        '''
        with open(file_path, 'r') as yamlfile:
            data = yaml.load(yamlfile, Loader=yaml.FullLoader)
            return data

    def write_yaml(data:dict, file_path):
        '''
        Write data to the yaml file.

        :param dict data: The data to write into the yaml file.
        :param str file_path: Path of the yaml file.fff
        '''
        with open(file_path, 'w') as file:
            yaml.dump(data, file)
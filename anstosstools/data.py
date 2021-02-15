'''
TODO - 

- Define Generic dynamic classes here,
  e.g. 
    class Nation
      allowed_fields = []
        -> Maybe a dictionary to allow type specifics?

      __setattr__ -> # https://stackoverflow.com/questions/7042152/how-do-i-properly-override-setattr-and-getattribute-on-new-style-classes

      __getattr__


!!! Maybe have the save file definitions in a python config file?
    - It's basically like json but easy to import and access without loading?
    - and if we just write json it's the same thing pretty much?
    - !!! CONS - the parser should not care which config it is and just get the config parsed, so json file is still the best in this case



idea: 
  main()
    - set config_path e.f. /parser/sav_parser/config/anstoss3/v1.40
    - new Config(config_path) -> in sav_config_manager
        - access to main config as attributes
        - access to each section config
    - sav_manager.load_sav_data(config, data_path)
    - sav_manager.get_generic_data (convert data to data.py format)
    - datamanager.save_json
    - datamanager.load_json
    - sav_manager.import_data_from_generic(config, sav_data)
    - sav_manager.write_save_data

'''


class GenericData():
    """Base class for generic data."""
    allowed_fields = []

    def __init__(self):
        for field in self.allowed_fields:
            setattr(self, field, None)

    def from_dict(self, data_dict):
        for field in self.allowed_fields:
            setattr(self, field, data_dict[field])

    def to_dict(self):
        data_dict = {}

        for field in self.allowed_fields:
            data_dict[field] = getattr(self, field)

        return data_dict

    def __setattr__(self, name, value):
        if name not in self.allowed_fields:
            raise AttributeError(F'Field name "{name}" not allowed for class "{type(self).__name__}"')

        super().__setattr__(name, value)


class Nation(GenericData):
    """A generic class representing data for a nation."""
    allowed_fields = [
        'Land', 'Unknown_02', 'Kuerzel', 'Unknown_04', 'Unknown_05', 'Unknown_06',
        'Unknown_07', 'Unknown_08', 'Unknown_09', 'Unknown_10', 'Unknown_11']

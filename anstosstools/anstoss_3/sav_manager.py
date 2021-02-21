
import json
import logging
import os

from anstosstools.data import (
    Nation,
)

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

SECTION_DEFINITIONS = {
    'NATION': {
        'id_field': 'Land',
        'class': Nation,
        'sav_pos_list': Nation.allowed_fields,
    }
}

SUPPORTED_FILES = [
    'LAENDER.SAV'
]

FILE_PREFIX_SUFFIX = {
    'LAENDER.SAV': ('%SECT%NATION', '%ENDSECT%NATION')
}

JSON_ENCODING = 'utf-8'
SAV_ENCODING = 'windows-1252'
#SAV_ENCODING = 'ISO-8859-1'  # using chardet, 71% probability
# SAV_ENCODING = "Windows-1250"
SECTION_START_PREFIX = '%SECT%'
SECTION_END_PREFIX = '%ENDSECT%'


class SavManager():
    def __init__(self):
        self.data = {}

        for section in SECTION_DEFINITIONS:
            self.data[section] = []

    def get_json_for_section(self, section_name):
        json_data = {}
        section_name = section_name.upper()
        id_field = SECTION_DEFINITIONS[section_name]['id_field']
        for section in self.data[section_name]:
            json_data[getattr(section, id_field)] = section.to_dict()

        return json_data

    def add_section_from_dict(self, section_name, json_dict):
        section = SECTION_DEFINITIONS[section_name]['class']()
        for field_name, value in json_dict.items():
            setattr(section, field_name, value)

        self.data[section_name].append(section)

    def parse_file(self, file_path):
        file_name = os.path.basename(file_path)
        logger.debug(F'FileName: {file_name}')

        with open(file_path, 'r', encoding=SAV_ENCODING) as file_ptr:
            section = None
            section_name = None
            section_line_count = None

            for line_num, line in enumerate(file_ptr, start=1):
                line = line.rstrip()

                # Ignore blank lines
                if not line:
                    continue

                logger.debug(F'LINE_NUM: {line_num} - {line}')
                # Ignore file opener line
                if line_num == 1:
                    logger.debug(F'  >> Ignore File Identifier: "{line}"')
                    continue

                # Ignore file prefix (extra section sourounding the file)
                if (line_num == 2) and (file_name.upper() in FILE_PREFIX_SUFFIX):
                    logger.debug(F'  >> Ignore File Opener: "{line}"')
                    continue

                # Ignore file closing line
                if section is None and line.startswith(SECTION_END_PREFIX):
                    logger.debug(F'  >> Ignore File Closer: "{line}"')
                    continue

                # Process data
                if line.startswith(SECTION_START_PREFIX):  # Check if Section Start
                    assert section is None
                    assert section_name is None
                    assert section_line_count is None
                    section_name = line.removeprefix(SECTION_START_PREFIX)
                    section = SECTION_DEFINITIONS[section_name]['class']()
                    section_line_count = 0
                    logger.debug(F'  >> Open Section: "{section_name}"')
                elif line.startswith(SECTION_END_PREFIX):  # Check if section end
                    assert section is not None
                    assert section_name is not None
                    assert section_line_count is not None
                    logger.debug(F'  >> Close Section: "{section_name}"')
                    self.data[section_name].append(section)
                    section = None
                    section_name = None
                    section_line_count = None
                else:  # Data line
                    assert section is not None
                    assert section_name is not None
                    assert section_line_count is not None
                    field_name = SECTION_DEFINITIONS[section_name]['sav_pos_list'][section_line_count]
                    setattr(section, field_name, line)
                    section_line_count += 1

    def write_sections_to_sav(self, file_path):
        for section_name, section_list in self.data.items():
            for section in section_list:
                pass


# TODO - WE NEED UNIT TESTS FOR THOSE 2 FUNCTIONS AS WELL
def convert_sav_dir_to_json(*, sav_dir, json_dir):
    sav_manager = SavManager()
    for file_name in os.listdir(sav_dir):
        if file_name.upper() in SUPPORTED_FILES:
            file_path = os.path.join(sav_dir, file_name)
            sav_manager.parse_file(file_path)

    for section_name in SECTION_DEFINITIONS:
        section_json = sav_manager.get_json_for_section(section_name)
        section_path = os.path.join(json_dir, section_name + '.json')
        with open(section_path, 'w', encoding=JSON_ENCODING) as file_ptr:
            json.dump(section_json, file_ptr, indent=4, sort_keys=True, ensure_ascii=False)


def convert_json_dir_to_sav(*, json_dir, sav_dir):
    sav_manager = SavManager()

    # Read the json files
    for file_name in os.listdir(json_dir):
        section_name = os.path.splitext(file_name)[0]
        if section_name.upper() in SECTION_DEFINITIONS:
            file_path = os.path.join(json_dir, file_name)
            with open(file_path, 'r', encoding=JSON_ENCODING) as file_ptr:
                file_dict = json.load(file_ptr)
                for _, section_dict in file_dict.items():
                    sav_manager.add_section_from_dict(section_name, section_dict)

    # Write the files to sav
    sav_manager.write_sections_to_sav(sav_dir)

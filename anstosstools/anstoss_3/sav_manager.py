
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
        'section_open_close_tags': True,
    }
}

FILE_DEFINITIONS = {
    'LAENDER.SAV': {
        'prefix_suffix': ('%SECT%NATION', '%ENDSECT%NATION'),
        'write_sections': ['NATION']
    }
}

JSON_ENCODING = 'utf-8'
SAV_ENCODING = 'windows-1252'
SAV_FILE_ID = '17373592'
SECTION_START_PREFIX = '%SECT%'
SECTION_END_PREFIX = '%ENDSECT%'


class SavManager():
    def __init__(self):
        self.data = {}

        for section_name in SECTION_DEFINITIONS:
            self.data[section_name] = []

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
        file_name = os.path.basename(file_path).upper()
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
                if (line_num == 2) and ('prefix_suffix' in FILE_DEFINITIONS[file_name]):
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

    def write_sav_file(self, dest_dir, file_name):
        data_lines = []

        file_name = file_name.upper()

        # Add file id number
        data_lines.append(SAV_FILE_ID)

        # Add File Prefix
        if 'prefix_suffix' in FILE_DEFINITIONS[file_name]:
            data_lines.append(FILE_DEFINITIONS[file_name]['prefix_suffix'][0])

        # Add File data
        data_lines += self._build_write_data(file_name)

        # Add file suffix
        if 'prefix_suffix' in FILE_DEFINITIONS[file_name]:
            data_lines.append(FILE_DEFINITIONS[file_name]['prefix_suffix'][1])

        # Trigger a final blank line
        data_lines.append('')

        file_path = os.path.join(dest_dir, file_name.capitalize())
        with open(file_path, 'w', encoding=SAV_ENCODING) as file_ptr:
            file_ptr.writelines('\n'.join(data_lines))

    def export_to_sav(self, out_dir):
        for file_name in FILE_DEFINITIONS:
            self.write_sav_file(out_dir, file_name)

    def _build_write_data(self, file_name):
        data_list = []

        file_name = file_name.upper()

        for file_name in FILE_DEFINITIONS:
            for write_section in FILE_DEFINITIONS[file_name]['write_sections']:
                for section in self.data[write_section]:
                    # Add section opener
                    if 'section_open_close_tags' in SECTION_DEFINITIONS[write_section]:
                        data_list.append('%SECT%' + write_section)

                    # Add fields
                    for field in SECTION_DEFINITIONS[write_section]['sav_pos_list']:
                        data_list.append(getattr(section, field))

                    # Add section closer
                    if 'section_open_close_tags' in SECTION_DEFINITIONS[write_section]:
                        data_list.append('%ENDSECT%' + write_section)

        return data_list


# TODO - WE NEED UNIT TESTS FOR THOSE 2 FUNCTIONS AS WELL
def convert_sav_dir_to_json(*, sav_dir, json_dir, sort_keys=True):
    sav_manager = SavManager()
    for file_name in os.listdir(sav_dir):
        if file_name.upper() in FILE_DEFINITIONS:
            file_path = os.path.join(sav_dir, file_name)
            sav_manager.parse_file(file_path)

    for section_name in SECTION_DEFINITIONS:
        section_json = sav_manager.get_json_for_section(section_name)
        section_path = os.path.join(json_dir, section_name + '.json')
        with open(section_path, 'w', encoding=JSON_ENCODING) as file_ptr:
            json.dump(section_json, file_ptr, indent=4, sort_keys=sort_keys, ensure_ascii=False)


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
    sav_manager.export_to_sav(sav_dir)


import os

from anstosstools.data import (
    Nation,
)

SECTION_DEFINITIONS = {
    'NATION': {
        'class': Nation,
        'sav_pos_list': Nation.allowed_fields,
    }
}

SUPPORTED_FILES = [
    'Laender.sav'
]

FILE_PREFIX_SUFFIX = {
    'LAENDER.SAV': ('%SECT%NATION', '%ENDSECT%NATION')
}

SAV_ENCODING = 'windows-1252'
SECTION_START_PREFIX = '%SECT%'
SECTION_END_PREFIX = '%ENDSECT%'


class SavManager():
    def __init__(self):
        self.data = {}

        for section in SECTION_DEFINITIONS:
            self.data[section] = []

    def _parse_file(self, file_path):
        file_name = os.path.basename(file_path)
        print('FileName:', file_name)

        with open(file_path, 'r', encoding=SAV_ENCODING) as file_ptr:
            section = None
            section_name = None
            section_line_count = None

            for line_num, line in enumerate(file_ptr, start=1):
                line = line.rstrip()

                print('LINE_NUM', line_num, line)
                # Ignore file opener line
                if line_num == 1:
                    print(F'  >> Ignore File Identifier: "{line}"')
                    continue

                # Ignore file prefix (extra section sourounding the file)
                if (line_num == 2) and (file_name.upper() in FILE_PREFIX_SUFFIX):
                    print(F'  >> Ignore File Opener: "{line}"')
                    continue

                # Ignore file closing line
                if section is None and line.startswith(SECTION_END_PREFIX):
                    print(F'  >> Ignore File Closer: "{line}"')
                    continue

                # Process data
                if line.startswith(SECTION_START_PREFIX):  # Check if Section Start
                    assert section is None
                    assert section_name is None
                    assert section_line_count is None
                    section_name = line.removeprefix(SECTION_START_PREFIX)
                    section = SECTION_DEFINITIONS[section_name]['class']
                    section_line_count = 0
                    print(F'  >> Open Section: "{section_name}"')
                elif line.startswith(SECTION_END_PREFIX):  # Check if section end
                    assert section is not None
                    assert section_name is not None
                    assert section_line_count is not None
                    print(F'  >> Close Section: "{section_name}"')
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

        print('DATA', self.data)

def convert_sav_dir_to_json(*, sav_dir, json_dir):
    pass


def convert_json_dir_to_sav(*, json_dir, sav_dir):
    pass


import os

import pytest

from anstosstools.anstoss_3.sav_manager import (
    SUPPORTED_FILES, SAV_ENCODING,
    convert_sav_dir_to_json, convert_json_dir_to_sav
)

ANSTOSS_3_SAV_INPUT_DIR = 'tests/anstosstools/integration/TestFiles/Anstoss3/v1.40'


def test_import_export_test_dir(tmpdir):

    # Setup test dirs
    json_dir = os.path.join(tmpdir, 'json')
    os.mkdir(json_dir)
    sav_out_dir = os.path.join(tmpdir, 'sav_out')
    os.mkdir(sav_out_dir)

    # Convert to json
    convert_sav_dir_to_json(sav_dir=ANSTOSS_3_SAV_INPUT_DIR, json_dir=json_dir)

    # convert back to sav
    convert_json_dir_to_sav(json_dir=json_dir, sav_dir=sav_out_dir)

    # compare supported files
    for file_name in SUPPORTED_FILES:
        in_file_path = os.path.join(ANSTOSS_3_SAV_INPUT_DIR, file_name)
        convert_file_path = os.path.join(sav_out_dir, file_name)

        print('in_file_path', in_file_path)
        print('convert_file_path', convert_file_path)

        assert os.path.exists(convert_file_path)

        with open(in_file_path, 'r', encoding=SAV_ENCODING) as in_file_ptr:
            with open(convert_file_path, 'r', encoding=SAV_ENCODING) as convert_file_ptr:
                in_file_list = list(in_file_ptr)
                convert_file_list = list(convert_file_ptr)

                assert len(in_file_list) == len(convert_file_list)

                for idx, line in enumerate(in_file_list):
                    assert line == convert_file_list[idx]

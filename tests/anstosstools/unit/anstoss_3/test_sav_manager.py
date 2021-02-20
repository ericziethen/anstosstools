
import os

from anstosstools.anstoss_3.sav_manager import SAV_ENCODING, SavManager


def write_test_file_from_lines(file_path, line_list):
    with open(file_path, 'w', encoding=SAV_ENCODING) as file_ptr:
        for line in line_list:
            file_ptr.write(line + '\n')


def test_convert_laender_sav(tmpdir):
    test_laender_sav_lines = [
        '17373592', '%SECT%NATION',
        '%SECT%NATION', 'Sonstige', '1', 'SON', '2', '3', '4', '5', '6', '7', '8', '9', '%ENDSECT%NATION',
        '%SECT%NATION', 'Deutschland', '11', 'DEU', '12', '13', '14', '15', '16', '17', '18', '19', '%ENDSECT%NATION',
        '%ENDSECT%NATION'
    ]

    test_file_path = os.path.join(tmpdir, 'laender.sav')
    print('test_file_path', test_file_path)
    write_test_file_from_lines(test_file_path, test_laender_sav_lines)

    sav_manager = SavManager()

    sav_manager.parse_file(test_file_path)
    assert len(sav_manager.data['NATION']) == 2

    nation_json = sav_manager.get_json_for_section('NATION')

    assert nation_json['Deutschland']['Land'] == 'Deutschland'
    assert nation_json['Deutschland']['Kuerzel'] == 'DEU'
    assert nation_json['Deutschland']['Kuerzel'] == 'DEU'

    assert nation_json['Sonstige']['Land'] == 'Sonstige'
    assert nation_json['Sonstige']['Kuerzel'] == 'SON'


def test_read_laender_sav_with_blank_extra_blank_line(tmpdir):
    test_laender_sav_lines = [
        '17373592', '%SECT%NATION',
        '%SECT%NATION', 'Deutschland', '', '11', 'DEU', '12', '13', '14', '15', '16', '17', '18', '19', '%ENDSECT%NATION',
        '%ENDSECT%NATION'
    ]

    test_file_path = os.path.join(tmpdir, 'laender.sav')
    print('test_file_path', test_file_path)
    write_test_file_from_lines(test_file_path, test_laender_sav_lines)

    sav_manager = SavManager()

    sav_manager.parse_file(test_file_path)
    assert len(sav_manager.data['NATION']) == 1

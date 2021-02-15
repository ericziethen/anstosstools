
import pytest

from anstosstools.data import Nation

VALID_NATION_FIELDS = [
    ('Land', 'Deutschland'),
    ('Unknown_02', 'Unknown_02'),
    ('Kuerzel', 'DEU'),
    ('Unknown_04', 'Unknown_04,'),
    ('Unknown_05', 'Unknown_05,'),
    ('Unknown_06', 'Unknown_06,'),
    ('Unknown_07', 'Unknown_07,'),
    ('Unknown_08', 'Unknown_08,'),
    ('Unknown_09', 'Unknown_09,'),
    ('Unknown_10', 'Unknown_10,'),
    ('Unknown_11', 'Unknown_11,'),
]
@pytest.mark.parametrize('field_name, value', VALID_NATION_FIELDS)
def test_create_nation_good_fields(field_name, value):
    nation = Nation()
    setattr(nation, field_name, value)
    assert getattr(nation, field_name) == value


INVALID_NATION_FIELDS = [
    ('UNEXPECTED_VALUE', 'Deutschland'),
    ('UNEXPECTED VALUE', 'Deutschland'),
    ('', 'Deutschland'),
]
@pytest.mark.parametrize('field_name, value', INVALID_NATION_FIELDS)
def test_create_nation_bad_field(field_name, value):
    nation = Nation()
    with pytest.raises(AttributeError):
        setattr(nation, field_name, value)


def test_to_dict():
    nation = Nation()
    nation.Land = 'Deutschland'
    nation.Unknown_02 = 'Unknown_02'
    nation.Kuerzel = 'DEU'
    nation.Unknown_04 = 'Unknown_04'
    nation.Unknown_05 = 'Unknown_05'
    nation.Unknown_06 = 'Unknown_06'
    nation.Unknown_07 = 'Unknown_07'
    nation.Unknown_08 = 'Unknown_08'
    nation.Unknown_09 = 'Unknown_09'
    nation.Unknown_10 = 'Unknown_10'
    nation.Unknown_11 = 'Unknown_11'

    dict_data = nation.to_dict()

    assert dict_data['Land'] == 'Deutschland'
    assert dict_data['Unknown_02'] == 'Unknown_02'
    assert dict_data['Kuerzel'] == 'DEU'
    assert dict_data['Unknown_04'] == 'Unknown_04'
    assert dict_data['Unknown_05'] == 'Unknown_05'
    assert dict_data['Unknown_06'] == 'Unknown_06'
    assert dict_data['Unknown_07'] == 'Unknown_07'
    assert dict_data['Unknown_08'] == 'Unknown_08'
    assert dict_data['Unknown_09'] == 'Unknown_09'
    assert dict_data['Unknown_10'] == 'Unknown_10'
    assert dict_data['Unknown_11'] == 'Unknown_11'


def test_from_dict():
    dict_data = {
        'Land': 'Deutschland',
        'Unknown_02': 'Unknown_02',
        'Kuerzel': 'DEU',
        'Unknown_04': 'Unknown_04',
        'Unknown_05': 'Unknown_05',
        'Unknown_06': 'Unknown_06',
        'Unknown_07': 'Unknown_07',
        'Unknown_08': 'Unknown_08',
        'Unknown_09': 'Unknown_09',
        'Unknown_10': 'Unknown_10',
        'Unknown_11': 'Unknown_11',
    }

    nation = Nation()

    dict_data = nation.from_dict(dict_data)

    assert nation.Land == 'Deutschland'
    assert nation.Unknown_02 == 'Unknown_02'
    assert nation.Kuerzel == 'DEU'
    assert nation.Unknown_04 == 'Unknown_04'
    assert nation.Unknown_05 == 'Unknown_05'
    assert nation.Unknown_06 == 'Unknown_06'
    assert nation.Unknown_07 == 'Unknown_07'
    assert nation.Unknown_08 == 'Unknown_08'
    assert nation.Unknown_09 == 'Unknown_09'
    assert nation.Unknown_10 == 'Unknown_10'
    assert nation.Unknown_11 == 'Unknown_11'

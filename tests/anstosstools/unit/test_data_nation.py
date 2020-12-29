
import pytest

from anstosstools.data import Nation

VALID_NATION_FIELDS = [
    ('Land', 'Deutschland'),
    ('Unknown_02', 'Unknown_02'),
    ('Kuerzel', 'DEU'),
    ('Unknown_03', 'Unknown_03,'),
    ('Unknown_04', 'Unknown_04,'),
    ('Unknown_05', 'Unknown_05,'),
    ('Unknown_06', 'Unknown_06,'),
    ('Unknown_07', 'Unknown_07,'),
    ('Unknown_08', 'Unknown_08,'),
    ('Unknown_09', 'Unknown_09,'),
    ('Unknown_10', 'Unknown_10,'),
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
    


'''
def test_save_to_json():

def test_read_from_json():
'''












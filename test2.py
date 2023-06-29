a = 'holamundo'

try:
    assert 'holamundo' in a
    # raise AssertionError
except AssertionError:
    print('hubo error')
finally:
    print('setermino')
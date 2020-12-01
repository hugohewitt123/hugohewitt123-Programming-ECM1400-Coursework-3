from covid import get_covid

def test_get_covid():
    assert get_covid() != "error getting covid info, api call error"
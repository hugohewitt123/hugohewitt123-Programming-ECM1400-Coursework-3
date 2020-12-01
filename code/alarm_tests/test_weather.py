from weather import weathers

def test_weathers():
    assert weathers() != [{'cod':'404','message':"FAILED couldn't get weather data"}]
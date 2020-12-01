from news import news

def test_new_news():
    lst = []
    assert news() != [{'title':'FAILED','content':"couldn't get news data"}]

def test_old_news():
    lst = [1]
    assert len(news()) > 0
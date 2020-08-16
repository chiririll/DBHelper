def test(**kwargs):
    db = kwargs['DB']
    return kwargs['message']


functions = {
    'test': test
}

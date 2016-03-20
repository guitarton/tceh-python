import pickle

STORAGE_FILE = 'storage.pickle'


class Storage:
    def __init__(self):
        self.articles = []

    def load(self):
        with open(STORAGE_FILE) as f:
            self.articles = pickle.load(f)

    def dump(self):
        with open(STORAGE_FILE, 'wb') as f:
            pickle.dump(self.articles, f)


class Articles:
    def __init__(self, title, body):
        self.title = title
        self.body = body

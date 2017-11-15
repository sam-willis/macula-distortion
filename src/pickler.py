import pickle


def save(key, obj):
    with open("./pickleobjs/{}".format(key), 'wb') as f:
        pickle.dump(obj, f)


def load(key):
    with open("./pickleobjs/{}".format(key), mode='rb') as f:
        return pickle.load(f)

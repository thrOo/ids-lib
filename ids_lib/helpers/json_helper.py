import json


def serialize_json(instance=None, path=None):
    dt = {}
    dt.update(vars(instance))

    with open(path, "w") as file:
        json.dump(dt, file, indent=8)
        print(json.dumps(dt, indent=8))


def deserialize_json(cls=None, path=None):
    def read_json(_path):
        with open(_path, "r") as file:
            return json.load(file)

    data = read_json(path)

    instance = object.__new__(cls)

    for key, value in data.items():
        setattr(instance, key, value)

    return instance

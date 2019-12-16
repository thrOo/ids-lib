import os


def load_file(path):
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            split = line.split()

            # do preprocessors here

            yield split


def load_dir(path):
    # if runs.csv exists use the given order,
    # else go through whole directory
    if os.path.isfile(os.path.join(path, "runs.csv")):
        with open(os.path.join(path, "runs.csv")) as f:
            lines = f.readlines()
            # removing column_names
            lines.pop(0)

            for line in lines[]:
                split = [x.strip() for x in line.split(",")]
                for x in load_file(os.path.join(path, split[1] + ".txt")):
                    yield x
    else:
        for file in os.listdir(path):
            if file.endswith(".txt"):
                for x in load_file(os.path.join(path, file)):
                    yield x


def dataset_generator(path):
    if os.path.isdir(path):
        return load_dir(path)
    elif os.path.isfile(path):
        return load_file(path)
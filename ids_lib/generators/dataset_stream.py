import os


def load_file(path):
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            split = line.split()

            # do preprocessors here

            yield split


def load_dir(path, start=0, count=None):
    """
    :param str path: file or dir path to dataset

    if path is a directory and runs.csv exits:
    :param int start: start index offset
    :param int count: number of files user wants
    """
    # TODO params validation
    # if runs.csv exists use the given order,
    # else go through whole directory
    if os.path.isfile(os.path.join(path, "runs.csv")):
        #calculate count offset
        if count is not None:
            count = count + start

        with open(os.path.join(path, "runs.csv")) as f:
            lines = f.readlines()
            # removing column_names
            lines.pop(0)

            for line in lines[start:count]:
                split = [x.strip() for x in line.split(",")]
                yield split[1] + ".txt"
                #for x in load_file(os.path.join(path, split[1] + ".txt")):
                #    yield x
    else:
        for file in os.listdir(path):
            if file.endswith(".txt"):
                for x in load_file(os.path.join(path, file)):
                    yield x


def dataset_generator(path, start=0, count=None):
    if os.path.isdir(path):
        return load_dir(path, start, count)
    elif os.path.isfile(path):
        return load_file(path)
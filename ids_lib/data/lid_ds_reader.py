import os
from ids_lib.generators.dataset_stream import dataset_generator
from ids_lib.generators.filter_stream import filter_generator


def load_file(path):
    with open(path) as f:
        lines = f.readlines()
        splitted = []
        for line in lines:
            splitted.append(line.split())
        return splitted


class LIDDSTextReader:
    """This is a reader class for a LID_DS recorded scenario with txt-files"""

    def __init__(self, path):
        self.infinite_running = False
        self.path = path
        self.normal_files = []
        self.attack_files = []

        # read runs.csv and create lists of filepaths sorted by behaviour
        try:
            with open(os.path.join(path, "runs.csv")) as f:
                lines = f.readlines()
                # removing column_headers line
                lines.pop(0)

                for line in lines:
                    split = [x.strip() for x in line.split(",")]
                    if split[2] == 'False':
                        self.normal_files.append(os.path.join(path, split[1] + ".txt"))
                    if split[2] == 'True':
                        self.attack_files.append(os.path.join(path, split[1] + ".txt"))

        except FileNotFoundError:
            print("runs.csv not found")

        print("dataset initialized( normal: "
              + str(len(self.normal_files))
              + " attack: "
              + str(len(self.attack_files)) + ")")

    def get_stream(self, behaviour, count=None, offset=0, filter_set=None):
        file_list = self.get_files(behaviour)
        # mind the count offset
        if count is not None:
            count = count + offset

        if filter_set is not None:
            for file in file_list[offset:count]:
                for x in filter_generator(dataset_generator(load_file(file)), filter_set):
                    yield x
        else:
            for file in file_list[offset:count]:
                for x in dataset_generator(load_file(file)):
                    yield x

    def get_infinite_stream(self, behaviour, count=None, offset=0, filter_set=None):
        self.infinite_running = True
        while self.infinite_running:
            for x in self.get_stream(behaviour, count, offset, filter_set):
                yield x
                if self.infinite_running is not True:
                    break

    def stop_infinite_stream(self):
        """
            this is not interup
        """
        self.infinite_running = False

    def get_files(self, behaviour):
        if behaviour == 'normal':
            return self.normal_files
        elif behaviour == 'attack':
            return self.attack_files
        else:
            raise Exception("invalid behaviour type")

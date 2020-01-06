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
    """This is a reader class for a LID_DS recorded scenario with txt-files

    Attributes
    ----------
    path : str
        directory path, where the recorded txt-files and the runs.csv lie
    normal_files : list of str
        array of single file paths with normal behaviour
    attack_files : list of str
        array of single file paths with attack behaviour
    infinite_running : boolean
        boolean to control the infinite_stream method
    Methods
    -------
    get_files(behaviour)
        returns array of specified behaviour files
    get_stream(behaviour, count=None, offset=0, filter_set=None)
        returns a item_generator in specified interval and applied filters
    get_infinite_stream(behaviour, count=None, offset=0, filter_set=None)
        wrapper around get_stream with infinite loop
    stop_infinite_stream()
        sets infinite_running to False and interupts infinite_stream loop
    """

    def __init__(self, path):
        """reads runs.csv to fill filepaths arrays
        Parameters
        ----------
         path : str
            directory path, where the recorded txt-files and the runs.csv lie
        """
        if not os.path.isdir(path):
            raise NotADirectoryError

        self.path = path
        self.normal_files = []
        self.attack_files = []
        self.infinite_running = False

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

        print("dataset reader initialized( normal: "
              + str(len(self.normal_files))
              + " attack: "
              + str(len(self.attack_files)) + ")")

    def get_files(self, behaviour):
        """returns array of specified behaviour files

        Parameters
        ----------
        behaviour : str
            type of behaviour (attack, normal)

        Raises
        ------
        Exception
            If behaviour type is unknown
        """
        if behaviour == 'normal':
            return self.normal_files
        elif behaviour == 'attack':
            return self.attack_files
        else:
            raise Exception("invalid/unknown behaviour type")

    def get_stream(self, behaviour, count=None, offset=0, filter_set=None):
        """returns a item_generator in specified interval and applied filters

        Parameters
        ----------
        behaviour : str
            type of behaviour (attack, normal)
        count : int, optional
            number of files to read (default= None, going through all of the files)
        offset : int, optional
            index of the array from where to start (default = 0)
        filter_set: dict, optional
            a filter_set with exclusions and/or trims (default = None)

            format of filter_set = {
                'exclude': {
                    column: 'str',
                    ...
                },
                'trim': [ column, ... ]
            }
        """
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
        """wrapper around get_stream with infinite loop

        Parameters
        ----------
        behaviour : str
            type of behaviour (attack, normal)
        count : int, optional
            number of files to read (default= None, going through all of the files)
        offset : int, optional
            index of the array from where to start (default = 0)
        filter_set: dict, optional
            a filter_set with exclusions and/or trims (default = None)

            format of filter_set = {
                'exclude': {
                    column: 'str',
                },
                'trim': [ column ]
            }
        """
        self.infinite_running = True
        while self.infinite_running:
            for x in self.get_stream(behaviour, count, offset, filter_set):
                yield x
                if self.infinite_running is not True:
                    break

    def stop_infinite_stream(self):
        """sets infinite_running to False and interupts infinite_stream loop"""
        self.infinite_running = False

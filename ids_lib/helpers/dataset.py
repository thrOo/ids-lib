import tempfile, os
from pick import pick
from ftplib import FTP_TLS
from datetime import datetime

def find_recording(scenario_name, recording_name):
    ftp = FTP_TLS('systemcalls.io')
    ftp.login('idslib','cH&rQ]M<PZ5PyeYRe#cc@]Xu\<MH?,S,C5gaMgcEh6t6')

    # Get All Files
    files = ftp.nlst()
    if scenario_name is None:
        scenario_name, index = pick(files, "Please select a scenario:")

    recordings = ftp.nlst(scenario_name)
    recording_filenames = [filepath.split('/')[-1] for filepath in recordings]
    runs_csv_index = recording_filenames.index("runs.csv")
    del recording_filenames[runs_csv_index]

    recording_names = [filename.split('.')[0] for filename in recording_filenames]
    if (recording_name is None) or (recording_name not in recording_names):
        recording_name, index = pick(recording_names, "Please select a recorded trace!")

    tmpdir = tempfile.gettempdir()
    filepath = "{}/{}.txt".format(scenario_name, recording_name)
    tmpfile_path = os.path.join(tmpdir, "{}.{}.txt".format(scenario_name, recording_name))
    if not os.path.exists(tmpfile_path):
        print("Downloading..." + filepath)
        ftp.retrbinary("RETR " + filepath, open(tmpfile_path, 'wb').write)
    else:
        print("Read recorded trace from cache!")
    ftp.close()

    return tmpfile_path

find_recording(None, None)

import os
from nltk import ngrams
import datetime
from datetime import timedelta
import numpy as np
import json
import argparse
from keras.models import load_model

threshhold = .55
fa = 0
dt = 0

og_syscalls = None
with open('og_syscalls.json') as f:
    og_syscalls = json.loads(f.read())


def ohe(category_id):
    ohe = np.full(len(og_syscalls)+1, 0)
    ohe[category_id - 1] = 1
    return list(ohe)

def lookup_syscall_id(syscall_name):
    if syscall_name in og_syscalls.keys():
        return og_syscalls[syscall_name]
    else:
        return len(og_syscalls)+1


def iso_to_ns(isostring):
    ts_split = isostring.split('.')
    ts = datetime.time.fromisoformat(ts_split[0])
    min = ts.hour * 60 + ts.minute
    seconds = min * 60 + ts.second
    ms = seconds * (10 ** 6) + ts.microsecond
    ns = ms * (10 ** 3) + int(ts_split[-1])
    return ns


def get_all_occurring_syscalls(input_list):
    result = set()
    for x in input_list:
        result.add(x)
    return list(result)


def before_after_exploit_ts_split(array, exploit_ts):
    array_before = []
    array_after = []
    if exploit_ts < 1:
        return [array, []]
    else:
        for x in array:
            if x[0] < exploit_ts:
                array_before.append(x)
            else:
                array_after.append(x)
        return [array_before, array_after]

def load_file(filepath, n, exploit_ts):
    with open(filepath) as f:
        lines = f.readlines()
        basetimestamp = lines[0].split()[0]
        basetime = iso_to_ns(basetimestamp)

        exploit_ts_ns = exploit_ts * (10 ** 9)
        relative_times = {}
        for x in lines:
            split = x.split()
            split[0] = iso_to_ns(split[0]) - basetime
            split[1] = int(split[1]) # thread id
            split.append(split[2])
            split[2] = ohe(lookup_syscall_id(split[2]))

            if split[2] is not None:
                if split[1] not in relative_times:
                    relative_times[split[1]] = []
                relative_times[split[1]].append(split)
        #occ_syscalls = get_all_occurring_syscalls([x[2] for x in relative_times])
        threadset = set()
        # Split before and after exploit_ts
        syscalls_splitted = relative_times.copy()
        for thread_id in relative_times.keys():
            syscalls_splitted[thread_id] = before_after_exploit_ts_split(relative_times[thread_id], exploit_ts_ns)

        ress = {}
        for thread_id in syscalls_splitted.keys():
            res = [list(ngrams(syscalls_splitted[thread_id][0], n)), list(ngrams(syscalls_splitted[thread_id][1], n))]
            ress[thread_id] = res
        return ress



def load_scenario(dirpath, n, exploit_ts):
    results = []
    for file in os.listdir(os.path.join(dirpath, "filtered")):
        if file.endswith("_filtered.txt"):
            res = load_file(os.path.join(dirpath, "filtered", file), n, exploit_ts)
            results.append(res)
    return results


#a = load_scenario("CVE-2017-7529", 5)
#print(a)
def __repr_generator(ress):
    for x in ress.keys():
        print(list(ress[x]))
        #for y in ress[x]:
        #    print(y)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some syscall trace file.')
    parser.add_argument('--file', nargs='?', help='a file to process')
    parser.add_argument('--dir', nargs='?', help='a directory to process')
    parser.add_argument('--n', nargs=1, help='n-gram length')
    parser.add_argument('--evaluate', help='n-gram length')
    parser.add_argument('--exploit', nargs='?', help='n-gram length', default=0)

    args = parser.parse_args()
    if not args.evaluate:
        if args.file is not None:
            __repr_generator(load_file(args.file, int(args.n[0]), int(args.exploit[0])))
        if args.dir is not None:
            ress = load_scenario(args.dir, int(args.n[0]), int(args.exploit[0]))
            for x in ress:
                __repr_generator(x)
    else:
        res = None
        if args.file is not None:
            res = load_file(args.file, int(args.n[0]), int(args.exploit[0]))
        if args.dir is not None:
            res = load_scenario(args.dir, int(args.n[0]), int(args.exploit[0]))

        model = load_model('test.h5')

        losses = []
        normal_ngrams_saved = []
        for thread_key in  res.keys():
            for i in range(len(res[thread_key])):
                input = []
                array = res[thread_key][i]
                ngram = [[dp[3] for dp in n_gram_datapoint] for n_gram_datapoint in array]
                if i == 0:
                    for gram in ngram:
                        normal_ngrams_saved.append(gram)

                    input = [np.concatenate([np.array(dp[2]) for dp in n_gram_datapoint]).flatten() for n_gram_datapoint in array]
                if i == 1:
                    for k in range(len(ngram)):
                        gram = ngram[k]
                        if not (gram in normal_ngrams_saved):
                            input = [np.concatenate([np.array(dp[2]) for dp in n_gram_datapoint]).flatten() for
                                     n_gram_datapoint in array]
                        else:
                            continue

                if i == 0:
                    if len(input) > 0:
                        for x in input:
                            loss = model.evaluate(np.array([x]), np.array([x]), verbose=0)[0]
                            losses.append(loss)
                            #print("{}::: {}; {}".format(('NORMAL: ' if i==0 else 'ANOMALOUS: '), x, loss))
                            if loss > threshhold:
                                fa+= 1
                if i == 1:
                    if len(input) > 0:
                        found_one = False
                        for x in input:
                            loss = model.evaluate(np.array([x]), np.array([x]), verbose=0)[0]
                            losses.append(loss)
                            #print("{}::: {}; {}".format(('NORMAL: ' if i==0 else 'ANOMALOUS: '), x, loss))
                            if loss > threshhold:
                                found_one = True
                        if found_one:
                            dt += 1

    print('{}, {}, {}, {}'.format(args.file.split('/')[-1], 'NORMAL' if int(args.exploit[0]) < 1 else 'EXPLOIT', fa, dt))

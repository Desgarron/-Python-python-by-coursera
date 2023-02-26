import json
import argparse
import os
import tempfile


parsim = argparse.ArgumentParser()
parsim.add_argument('--key')
parsim.add_argument('--value', default=None)

args = parsim.parse_args()
key = args.key
value = args.value

storage_file = os.path.join(tempfile.gettempdir(), 'storage.data')

if key and value and os.path.exists(storage_file):
    with open(storage_file, 'r') as rd:
        to_dict = json.load(rd)
        with open(storage_file, 'w') as f:
            if key in to_dict:
                # append value to new key
                to_dict[key].append(value)
            else:
                # create new key:value
                to_dict[key] = [value]
            json.dump(to_dict, f, indent=1)
else:
    if not os.path.exists(storage_file):
        with open(storage_file, 'w') as wd:
            json.dump({key: [value]}, wd, indent=1)

    elif value is None:
        with open(storage_file, 'r') as rd:
            data = json.load(rd)
            print(*data.get(key, [None]), sep=', ')

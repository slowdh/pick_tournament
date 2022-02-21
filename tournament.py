
DEBUG = True

names = ['DH Kim', 'GM lee', 'JW Kim']
people_file_paths = ['dh_path.txt', 'gm_path.txt', 'jw_path.txt']
ret = []

if DEBUG:
    ret = [1, 2, 1]
else:
    result = 1
    for path in people_file_paths:
        with open(path) as f:
            pass
        ret.append(result)
assert ret == [1, 2, 1]

for idx, val in enumerate(ret):
    name = names[idx]
    print(f"{name} vote: {val}")

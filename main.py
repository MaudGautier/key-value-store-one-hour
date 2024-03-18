import os

DATABASE = "./datafiles/"
SEPARATOR = ","
HASH_INDEX = {}
THRESHOLD = 30  # Max number of bytes in each datafile


# UTILS
def list_files():
    return [f"{DATABASE}/{filename}" for filename in sorted(os.listdir(DATABASE))]


def select_datafile():
    all_files = list_files()
    if len(all_files) == 0:
        return f"{DATABASE}/0.txt"

    current_file = all_files[-1]
    with open(current_file, "a") as f:
        offset = f.tell()
        # Create new file if too big
        if offset > THRESHOLD:
            index = len(all_files)
            return f"{DATABASE}/{index}.txt"

    return current_file


def create_record(key, value):
    return f"{key}{SEPARATOR}{value}\n"


def clear():
    for file in os.listdir(DATABASE):
        os.remove(f"{DATABASE}/{file}")


# DATABASE
def set(key, value):
    # o(1)
    file = select_datafile()
    record = create_record(key, value)
    with open(file, "a") as f:
        offset = f.tell()
        f.write(record)
        HASH_INDEX[key] = (file, offset)


def get(key):
    # o(1)
    if key not in HASH_INDEX:
        return None

    file, offset = HASH_INDEX[key]
    with open(file, "r") as f:
        f.seek(offset)
        line = f.readline()
        value = line[len(f"{key}{SEPARATOR}"):-1]

    return value


def compact(infile, outfile):
    kv_pairs = {}
    with open(infile, "r") as f:
        lines = f.readlines()
        for line in lines:
            key, _ = line[:-1].split(SEPARATOR)
            kv_pairs[key] = line

    with open(outfile, "w") as f:
        for key, line in kv_pairs.items():
            offset = f.tell()
            f.write(line)
            HASH_INDEX[key] = (outfile, offset)

    os.remove(infile)


# TESTING
if __name__ == "__main__":
    clear()

    print("---- SET KEY-VALUES ---- ")
    set("key1", "value1")
    set("key2", "value2")
    set("key1", "another_value1")
    set("key1", "yet_another_value1")
    set("key2", "another_value2")
    set("key1", "i_need_yet_another_value1")

    print("--- GET VALUES ----- ")
    for key in ["key1", "key2", "key3"]:
        print(f"Value for key '{key}' is {get(key)}")

    print("---- COMPACT ---- ")
    infile = f"{DATABASE}/0.txt"
    outfile = f"{DATABASE}/0_compacted.txt"
    compact(infile, outfile)

    print("--- GET VALUES ----- ")
    for key in ["key1", "key2", "key3"]:
        print(f"Value for key '{key}' is {get(key)}")

import os

# ------------------------------------------------------------------------------------------------------------------- #
#                                                      CONSTANTS                                                      #
# ------------------------------------------------------------------------------------------------------------------- #

DATABASE = "./datafiles"
SEPARATOR = ","
HASH_INDEX = {}
THRESHOLD = 30  # Max number of bytes in each datafile


# ------------------------------------------------------------------------------------------------------------------- #
#                                               UTILS (HELPER FUNCTIONS)                                              #
# ------------------------------------------------------------------------------------------------------------------- #

def list_datafiles():
    """Lists all datafiles.
    They are sorted by name. Therefore, the oldest files are at the beginning of the list and the most recent ones at
    the end (see `select_datafile` to see how names of files are defined).
    """
    return [f"{DATABASE}/{filename}" for filename in sorted(os.listdir(DATABASE))]


def select_datafile():
    """Selects the datafile to write into.
    The logic is the following:
    - as long as the current datafile is smaller than the `THRESHOLD`, we keep on writing to it
    - as soon as it gets bigger than the `THRESHOLD`, we define a new datafile, whose name is the next index (thus the
      length of the list of files since we start from index 0).
    """
    all_datafiles = list_datafiles()

    # Edge case: No file exists yet => the first datafile is `0.txt`
    if len(all_datafiles) == 0:
        return f"{DATABASE}/0.txt"

    # Regular case: look at the size of the most recent datafile to decide which to select
    current_file = all_datafiles[-1]
    file_size = os.path.getsize(current_file)

    # If the current file is bigger than the `THRESHOLD`, select a new datafile
    if file_size > THRESHOLD:
        index = len(all_datafiles)
        return f"{DATABASE}/{index}.txt"

    # Otherwise, select the current file
    return current_file


def create_record(key, value):
    """Formats the record."""
    return f"{key}{SEPARATOR}{value}\n"


def clear():
    """Clears the database by deleting all existing datafiles."""
    for file in os.listdir(DATABASE):
        os.remove(f"{DATABASE}/{file}")


# ------------------------------------------------------------------------------------------------------------------- #
#                                                       DATABASE                                                      #
# ------------------------------------------------------------------------------------------------------------------- #

def set(key, value):
    """Sets a new key and value by appending the record to the datafile.
    Time complexity for insertion is o(1).
    """
    file = select_datafile()
    record = create_record(key, value)
    with open(file, "a") as f:
        offset = f.tell()
        f.write(record)
        HASH_INDEX[key] = (file, offset)


def get(key):
    """Retrieves the value associated to a given key by looking up in the hash index in which file and at which byte
    offset it is located.
    Time complexity for lookups is o(1) thanks to the hash index (this requires one lookup in the hash table and one
    single disk seek).
    """
    # Case where the key does not exist
    if key not in HASH_INDEX:
        return None

    # Key is in the hash index => do one disk seek to fetch it in the corresponding file
    file, offset = HASH_INDEX[key]
    with open(file, "r") as f:
        f.seek(offset)
        line = f.readline()
        value = line[len(f"{key}{SEPARATOR}"):-1]

    return value


def merge(infiles, outfile):
    """Compacts and merges multiple datafiles into one.
    The datafiles passed as parameters must be sorted from oldest to most recent, because the first step consists in
    reading them all and storing them in memory, thus replacing every previously read value by the newly read one.
    So, for this to work, it is essential that input files are sorted in the oldest-to-newest order.
    """

    # First, record all key-value pairs in memory by reading all files one by one
    kv_pairs = {}
    for infile in infiles:
        with open(infile, "r") as f:
            lines = f.readlines()
            for line in lines:
                key, _ = line[:-1].split(SEPARATOR)
                kv_pairs[key] = line

    # Second, write all recorded key-value pairs (the most recent value for each key) to the merged file
    with open(outfile, "w") as f:
        for key, line in kv_pairs.items():
            offset = f.tell()
            f.write(line)
            HASH_INDEX[key] = (outfile, offset)

    # Last, reclaim disk space by deleting all input files
    for infile in infiles:
        os.remove(infile)


# ------------------------------------------------------------------------------------------------------------------- #
#                                                       TESTING                                                       #
# ------------------------------------------------------------------------------------------------------------------- #

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

    print("---- MERGE ALL FILES INTO ONE ---- ")
    all_datafiles = list_datafiles()
    outfile = f"{DATABASE}/merged.txt"
    merge(all_datafiles, outfile)

    print("--- GET VALUES ----- ")
    for key in ["key1", "key2", "key3"]:
        print(f"Value for key '{key}' is {get(key)}")

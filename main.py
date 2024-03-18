import os

DATABASE = "./datafiles/"
SEPARATOR = ","


# UTILS
def select_datafile():
    return f"{DATABASE}/0.txt"


def create_record(key, value):
    return f"{key}{SEPARATOR}{value}\n"


# DATABASE
def set(key, value):
    # o(1)
    file = select_datafile()
    record = create_record(key, value)
    with open(file, "a") as f:
        f.write(record)


# TESTING
if __name__ == "__main__":
    print("---- SET KEY-VALUES ---- ")
    set("key1", "value1")
    set("key2", "value2")
    set("key1", "another_value1")
    set("key1", "yet_another_value1")


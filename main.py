import os

DATABASE = "./datafiles/"
SEPARATOR = ","


# UTILS
def select_datafile():
    return f"{DATABASE}/0.txt"


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
        f.write(record)


def get(key):
    # o(n)
    file = select_datafile()
    value = None
    with open(file, "r") as f:
        for line in f:
            if line.startswith(f"{key}{SEPARATOR}"):
                value = line[len(f"{key}{SEPARATOR}"):-1]
    return value


# TESTING
if __name__ == "__main__":
    clear()

    print("---- SET KEY-VALUES ---- ")
    set("key1", "value1")
    set("key2", "value2")
    set("key1", "another_value1")
    set("key1", "yet_another_value1")

    print("--- GET VALUES ----- ")
    for key in ["key1", "key2", "key3"]:
        print(f"Value for key '{key}' is {get(key)}")

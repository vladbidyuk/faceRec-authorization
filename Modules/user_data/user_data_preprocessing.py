import pickle
import numpy
import os

# data_struct:
# { "id_01": ["John Smith", "Green", "Available", numpy.array([1,2,3...68])],
#   "id_02": ["Max Paine", "Red", "Unavailable", numpy.array([1,2,3...68])] }


class User:
    def __init__(self, full_name, group, status, specs):
        self.full_name = full_name
        self.group = group
        self.status = status
        self.specs = specs

    def __str__(self):
        return "[{} | {} | {} | {}]".format(self.full_name, self.group, self.status, self.specs)


class FileHandler:
    def __init__(self, file_location="UserData.txt"):
        self.file_location = file_location
        self.user_data_dict = {}

        if (os.path.isfile(self.file_location)):
            self.read_file()
        else:
            print("File not found!")

        self.user_count = len(self.user_data_dict)

    # Add new user into dictionary and increment count of users by one
    def add_user(self, user_data):
        self.user_data_dict[int(self.user_count+1)] = user_data
        self.user_count += 1

    # Remove user by name works well, but keys stay same and
    # values are overwritten. After removing records should be
    # rewritten "self.user_data_dict" starting with key from 1
    def remove_user_by_name(self, user_name):
        list_of_keys = []

        # Found keys for looked name
        for key, value in self.user_data_dict.items():
            if value.full_name == user_name:
                list_of_keys.append(key)

        # Remove all records with found keys
        for i in list_of_keys:
            self.user_data_dict.pop(i, None)
            self.user_count -= 1

    def read_file(self):
        with open(self.file_location, 'rb') as handle:
            self.user_data_dict = pickle.loads(handle.read())

    def write_file(self):
        with open(self.file_location, 'wb') as handle:
            pickle.dump(self.user_data_dict, handle)


def main():
    test_usr = User("John Smith", "Green", "Available", [1,2,3])
    test_usr1 = User("Tom Smith", "Green", "Available", [1, 2, 3])
    file_handler = FileHandler()
    file_handler.add_user(test_usr)
    file_handler.add_user(test_usr1)

    for key, value in file_handler.user_data_dict.items():
        print(key, ": ", value)

    file_handler.remove_user_by_name("John Smith")

    file_handler.write_file()
    file_handler.read_file()

    for key, value in file_handler.user_data_dict.items():
        print("After. {} : {}".format(key, value))

if __name__ == "__main__":
    main()
#!/usr/bin/env python

import argparse
import pickle
import os

''' data_struct: { 
 "John Smith": ["John Smith", "Green", "Available", numpy.array([1,2,3...68])],
 "Max Paine": ["Max Paine", "Red", "Unavailable", numpy.array([1,2,3...68])],
 ... } '''


class User:
    def __init__(self, full_name, group, status, specs):
        self.full_name = full_name
        self.group = group
        self.status = status
        self.specs = specs

    def __str__(self):
        return "[{} | {} | {} | {}]".format(self.full_name, self.group, self.status, self.specs)


class FileHandler:
    def __init__(self, file_location="UserData"):
        self.file_location = file_location
        self.user_data_dict = {}

        if (os.path.isfile(self.file_location)):
            self.read_file()
        else:
            print("File not found!")

    def __str__(self):
        for key, value in self.user_data_dict.items():
            print("{}: {}".format(key, value))
        return ''

    # Add new user into dictionary and increment count of users by one
    def add_user(self, user_data):
        self.user_data_dict[user_data.full_name] = user_data
        self.write_file()

    # Remove user by name (key value)
    def remove_user_by_name(self, user_name):
        list_of_keys = []

        # Found keys for looked name
        for key, value in self.user_data_dict.items():
            if key == user_name:
                list_of_keys.append(key)

        # Remove all records with found keys
        for i in list_of_keys:
            self.user_data_dict.pop(i, None)

        self.write_file()

    def read_file(self):
        with open(self.file_location, 'rb') as handle:
            self.user_data_dict = pickle.loads(handle.read())

    def write_file(self):
        with open(self.file_location, 'wb') as handle:
            pickle.dump(self.user_data_dict, handle)

def addUserInput():
    while(True):
        full_name = input("Enter full name: ")
        group = input("Enter user group [Green, Yellow, Red]: ")
        status = input("Enter user status [Available, Unavailable]: ")

        # Here should be started function which scan face few times and
        # calculate average parameters of face.
        specs = [1, 2, 3]

        if full_name is None or group is None or status is None or specs is None:
            print("Some value equal None, retype data !")
            print("Entered data looks: [{} | {} | {} | {}]".format(full_name, group, status, specs))
        else:
            break

    return User(full_name, group, status, specs)

def main():
    # ==============================================================================
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", required=True, choices=["add", "remove", "show"],
                        help="action for user data file management ...")
    args = vars(parser.parse_args())
    # ==============================================================================

    # init fileHandler object
    fileHanlder = FileHandler()

    if(args['action'] == "add"):
        fileHanlder.add_user(addUserInput())

    elif(args['action'] == "remove"):
        if len(fileHanlder.user_data_dict) != 0:
            print("List of available users: \n", fileHanlder)
            user = input("Enter full name: ")
            fileHanlder.remove_user_by_name(user)
        else:
            print("Not found available users!")

    elif(args['action'] == "show"):
        if len(fileHanlder.user_data_dict) != 0:
            print("List of available users:\n", fileHanlder)
        else:
            print("Not found available users!")

    else:
        # Should not happen such as handled by choices in parser
        print("Unknown action selected!")

if __name__ == "__main__":
    main()
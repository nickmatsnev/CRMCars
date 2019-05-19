import datetime
import os
import sys

from lib import constants


class StdoutRedirector:
    # pending_output stores any output passed to write where a \n has not yet been found
    __pending_output = ''
    __name = ''

    def __init__(self, name):
        self.__name = name

    def write(self, message):
        from os.path import expanduser
        home = expanduser("~")
        filename = constants.LOG_FILE_FORMAT_STRING.format(self.__name)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'a+') as f:
            output = self.__pending_output + message
            (output, not_used, self.__pending_output) = output.rpartition('\n')
            if output != '':
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                output = "[" + self.__name + "]" + "[" + timestamp + "] " + output.replace("\n",
                                                                                           "\n" + timestamp + " ")
                try:
                    print(output, file=f)
                    f.flush()
                except:
                    print("problem with file output of log")
                try:
                   print(output, file=sys.__stdout__)
                except:
                   print("Possible broken pipe:"+output,file=f)

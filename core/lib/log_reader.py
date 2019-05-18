import sys

sys.path.append('../../')
sys.path.append('../')
from core.lib import constants


def read_log(processor):
    logs = ""
    filename = constants.LOG_FILE_FORMAT_STRING.format(processor)
    with open(filename, 'r') as f:
        lines = tail(f, 400, 4096)
        for line in lines:
            logs += line + line.strip()
        return logs.__str__()


def tail(f, n=1, _buffer=1):
    """Tail a file and get X lines from the end"""
    # place holder for the n found
    lines = []

    block_counter = -1

    while True:
        try:
            import os
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  # either file is too small, or too many n requested
            f.seek(0)
            return f.readlines()

        lines = f.readlines()

        # we found enough, get out
        if len(lines) > n:
            return lines[-n:]

        # decrement the block counter to get the next X bytes
        block_counter -= 1

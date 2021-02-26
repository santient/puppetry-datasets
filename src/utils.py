import sys
import subprocess
import os


def run_command(command):
    return subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr,
                          shell=True, check=True)


def get_immediate_subdirectories(a_dir):
    """
    Fetch all the immediate subdirectory names in the current directory that
    don't start with a period.
    """
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name)) and name[0] != '.']

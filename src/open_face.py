import sys
import subprocess

def run_command(command):
    return subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr, shell=True, check=True)

videoPathWav=""
run_command(f"FeatureExtraction -f '{videoPathWav}'")
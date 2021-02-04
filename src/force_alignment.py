import module_manager
module_manager.review()
import sys
from p2fa import align

def force_align(wavFile, trsFile, outFile):
    align.align(wavFile, trsFile, outfile=outFile)

def remove_timestamps_captions(filePath):
    with open(filePath, 'r+') as file:
        data = file.read()
        newData=""
        for line in data.splitlines():
            if(line!="" and not line[0].isnumeric()):
                newData+=line+"\n"
        deleteFileContent(file)
        file.writelines(newData)

def deleteFileContent(file):
    file.seek(0)
    file.truncate()

force_align('/Users/kaajal/research/video.wav', '/Users/kaajal/research/captions.txt', "/Users/kaajal/research/output.TextGrid")
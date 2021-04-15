import os
import subprocess
import sys
from p2fa import align
import librosa
import numpy as np
from src.utils import *


def extract_frames(args):
    dirs = get_immediate_subdirectories(args.out_dir)
    for d in dirs:
        # video path is created in download.py
        root_path = os.path.join(args.out_dir, d)
        video_path = os.path.join(root_path, 'video.mp4')
        
        # frame rate same as video
        cmds = ['ffmpeg','-i',f'{video_path}', f'{root_path}/frames/frame%d.jpg']
        ffmpeg = subprocess.run(cmds)

        # raises CalledProcessError if exit code not 0
        ffmpeg.check_returncode()


def extract_waveforms(args):
    """
    Extract waveforms in a wav file for every video file.
    """
    save_dir = args.out_dir
    sr = args.sample_rate
    for vid_id in get_immediate_subdirectories(save_dir):
        video_path = os.path.join(save_dir, vid_id, 'video.mp4')
        audio_path = os.path.join(save_dir, vid_id, 'audio.wav')
        subprocess.call(['ffmpeg', '-y', '-i', video_path, '-ar', sr, audio_path])


def extract_spectrograms(args):
    """
    Construct and return the short-time fourier transformations and the mel
    spectrograms of all the audio files.
    """
    save_dir = args.out_dir
    for vid_id in get_immediate_subdirectories(save_dir):
        audio_path = os.path.join(save_dir, vid_id, 'audio.wav')
        y, sr = librosa.load(audio_path, sr=None)
        n_fft = args.n_fft
        n_mels = args.n_mels
        fft = librosa.stft(y, n_fft=n_fft)

        mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft,
                                                   n_mels=n_mels)
        mel_spect = librosa.power_to_db(mel_spect, ref=np.max)

        spec_dic = {}
        spec_dic['ft'] = fft
        spec_dic['mel_spect'] = mel_spect
        np.save(os.path.join(save_dir, vid_id, 'spectrogram.npy'), spec_dic)


def force_align(args):
    save_dir = args.out_dir
    for vid_id in get_immediate_subdirectories(save_dir):
        wavFile = os.path.join(save_dir, vid_id, 'audio.wav')
        trsFile = os.path.join(save_dir, vid_id, 'captions.txt')
        outFile = os.path.join(save_dir, vid_id, 'aligned.TextGrid')
        remove_timestamps_captions(trsFile)
        align.align(wavFile, trsFile, outfile=outFile)


def remove_timestamps_captions(filePath):
    with open(filePath, 'r+') as file:
        data = file.read()
        newData=""
        for line in data.splitlines():
            if(line!="" and not line[0].isnumeric()):
                newData+=line+"\n"
        deleteFileContent(file) # TODO see if unnecessary
        file.writelines(newData)


def deleteFileContent(file):
    file.seek(0)
    file.truncate()


def run_openface(args):
    save_dir = args.out_dir
    for vid_id in get_immediate_subdirectories(save_dir):
        videoPath = os.path.join(save_dir, vid_id, 'video.mp4')
        run_command(f"FeatureExtraction -f '{videoPath}'")


def extract_features(args):
    extract_frames(args)
    extract_waveforms(args)
    extract_spectrograms(args)
    force_align(args)
    run_openface(args)

import librosa
import numpy as np
import os
import subprocess


def get_immediate_subdirectories(a_dir):
    """
    Fetch all the immediate subdirectory names in the current directory that
    don't start with a period.
    """
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name)) and name[0] != '.']


def extract_waveforms(args):
    """
    Extract waveforms in a wav file for every video file.
    """
    save_dir = args.out_dir
    for vid_id in get_immediate_subdirectories(save_dir):
        video_path = os.path.join(save_dir, vid_id, 'video.mp4')
        audio_path = os.path.join(save_dir, vid_id, 'audio.mp4')
        subprocess.call(['ffmpeg', '-y', '-i', video_path, audio_path])


def extract_spectrograms(args):
    """
    Construct and return the short-time fourier transformations and the mel
    spectrograms of all the audio files.
    """
    save_dir = args.out_dir
    spec_dic = {}
    for vid_id in get_immediate_subdirectories(save_dir):
        audio_path = os.path.join(save_dir, vid_id, 'audio.mp4')
        y, sr = librosa.load(audio_path, sr=None)
        n_fft = args.spec.n_fft
        n_mels = args.spec.n_mels
        hop_length = args.spec.hop_length
        fft = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)

        mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft,
                                                   hop_length=hop_length,
                                                   n_mels=n_mels)
        mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
        spec_dic[vid_id] = {'ft': fft, 'mel_spect': mel_spect}
    return spec_dic


# TODO add methods
def extract_features(args):
    extract_frames(args)
    extract_waveforms(args)
    extract_spectrograms(args)
    force_align(args)
    run_openface(args)

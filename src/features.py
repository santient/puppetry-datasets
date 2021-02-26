import librosa
import numpy as np
from src.utils import *


def extract_waveforms(args):
    """
    Extract waveforms in a wav file for every video file.
    """
    save_dir = args.out_dir
    sr = args.sampling_rate
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
        n_fft = args.spec.n_fft
        n_mels = args.spec.n_mels
        fft = librosa.stft(y, n_fft=n_fft)

        mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft,
                                                   n_mels=n_mels)
        mel_spect = librosa.power_to_db(mel_spect, ref=np.max)

        spec_dic = {}
        spec_dic['ft'] = fft
        spec_dic['mel_spect'] = mel_spect
        np.save(os.path.join(save_dir, vid_id, 'spectrogram.npy'), spec_dic)


# TODO add methods
def extract_features(args):
    extract_frames(args)
    extract_waveforms(args)
    extract_spectrograms(args)
    force_align(args)
    run_openface(args)

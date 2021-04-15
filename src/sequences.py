import numpy as np
import h5py
from mmsdk import mmdatasdk
from src.utils import *


def read_spectrograms(args, video_id, start, end):
    save_dir = args.out_dir
    intervals = []
    features = []
    t = start

    # hop length is default n_fft/4, so only a quarter of window is unique
    spectro_unique_samples = args.n_fft / 4
    spectro_column_time = spectro_unique_samples / args.sampling_rate

    spectrogram = np.load(os.path.join(save_dir, video_id, "spectrogram.npy"))
    for i, spectro in enumerate(spectrogram.T):
        timestamp = i * spectro_column_time
        if start <= timestamp <= end:
            # spectro = np.stack([spectro.real, spectro.imag])
            intervals.append([t, timestamp])
            features.append(spectro.flatten())
            t = timestamp
    return np.array(intervals), np.array(features)


def spectrograms_to_compseq(args):
    spectrogram_data = {}
    save_dir = args.out_dir
    for video in get_immediate_subdirectories(save_dir):
        phone_intervals = list(h5py.File(os.path.join(save_dir, video,
                                                      "AlignFilter/{}_phones.hdf5".format(
                                                          video)))[video][
                                                      "intervals"])
        start = phone_intervals[0][0]
        end = phone_intervals[-1][1]
        spectrogram_intervals, spectrogram_features = read_spectrograms(video,
                                                                        start,
                                                                        end)
        spectrogram_data[video] = {}
        spectrogram_data[video]["intervals"] = spectrogram_intervals
        spectrogram_data[video]["features"] = spectrogram_features
    spectrograms = mmdatasdk.computational_sequence("spectrograms")
    spectrograms.setData(spectrogram_data, save_dir)
    spectrograms.deploy(os.path.join(save_dir, "spectrograms.csd"))


def read_words(args, video):
    save_dir = args.out_dir
    data = h5py.File(os.path.join(save_dir, video,
                                  "AlignFilter/{}_words.hdf5".format(video)))[
        video]
    intervals = list(data["intervals"])
    features = list(data["features"])
    return np.array(intervals), np.array(features)


def words_to_compseq(args):
    word_data = {}
    save_dir = args.out_dir
    for video in get_immediate_subdirectories(save_dir):
        word_intervals, word_features = read_words(args, video)
        word_data[video] = {}
        word_data[video]["intervals"] = word_intervals
        word_data[video]["features"] = word_features
    words = mmdatasdk.computational_sequence("words")
    words.setData(word_data, save_dir)
    words.deploy(os.path.join(save_dir, "words.csd"))


def read_phones(args, video):
    save_dir = args.out_dir
    data = h5py.File(os.path.join(save_dir, video,
                                  "AlignFilter/{}_phones.hdf5".format(video)))[
        video]
    intervals = list(data["intervals"])
    features = list(data["features"])
    return np.array(intervals), np.array(features)


def phones_to_compseq(args):
    phone_data = {}
    save_dir = args.out_dir
    for video in get_immediate_subdirectories(save_dir):
        phone_intervals, phone_features = read_phones(args, video)
        phone_data[video] = {}
        phone_data[video]["intervals"] = phone_intervals
        phone_data[video]["features"] = phone_features
    phones = mmdatasdk.computational_sequence("phones")
    phones.setData(phone_data, save_dir)
    phones.deploy(os.path.join(save_dir, "phones.csd"))


def make_computational_sequences(args):
    frames_to_compseq(args)
    masked_frames_to_compseq(args)
    waveforms_to_compseq(args)
    spectrograms_to_compseq(args)
    words_to_compseq(args)
    phones_to_compseq(args)
    openface_to_compseq(args)
    # align_computational_sequences(args)
    # compress_computational_sequences(args)

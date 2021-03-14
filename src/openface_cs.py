import os
import glob
from mmsdk import mmdatasdk
import numpy
import pandas
import h5py
import tqdm
import skimage.io
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import librosa

import warnings
warnings.filterwarnings("ignore")

def read_openface(video, start, end):
    openface_df = pandas.read_csv(os.path.join(root, video, "processed/{}.csv".format(video)), sep=", ")
    intervals = []
    features = []
    t = start
    for i, row in openface_df.iterrows():
        timestamp = float(row["timestamp"])
        confidence = float(openface_df.loc[openface_df["frame"] == frame].iloc[0]["confidence"])
        if timestamp >= start and timestamp <= end and confidence >= 0.9:
            intervals.append([t, timestamp])
            features.append(row.values[5:])
            t = timestamp
    return numpy.array(intervals), numpy.array(features)
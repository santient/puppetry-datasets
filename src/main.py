import argparse

from src.download import download_videos
from src.features import extract_features
from src.sequences import make_computational_sequences


def get_args():  
    parser = argparse.ArgumentParser(description="Build multimodal dataset.")
    parser.add_argument("--url_file", type=str, help="File with video URL list.")
    parser.add_argument("--out_dir", type=str, help="Output directory for dataset.")
    parser.add_argument("--res", type=str, default="1920:1080")
    parser.add_argument("--frame_rate", type=int, default=20)
    parser.add_argument("--lang", type=str, default="en")
    parser.add_argument("--sample_rate", type=int, default=8192)
    parser.add_argument("--n_fft", type=int, default=1024)
    parser.add_argument("--n_mels", type=int, default=128)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    download_videos(args)
    extract_features(args)
    make_computational_sequences(args)

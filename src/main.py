import argparse

from src.download import download_videos
from src.features import extract_features
from src.sequences import make_computational_sequences


def get_args():  
    parser = argparse.ArgumentParser(description="Build multimodal dataset.")
    parser.add_argument("url_file", type=str, help="File with video URL list.")
    parser.add_argument("out_dir", type=str, help="Output directory for dataset.")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    download_videos(args)
    extract_features(args)
    make_computational_sequences(args)

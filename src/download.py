import os
import pytube


def download_videos(args):
    """
    Downloads the list of YouTube videos and accompanying English subtitles from
    provided URLs
    :param args: List of YouTube video URLs
    """
    for url in args.url_file:
        try:
            source = pytube.YouTube(url)
        except:
            raise ValueError(f''''{url}' is not a valid URL''')
        video = source.streams.get_highest_resolution()
        video_id = pytube.extract.video_id(url)
        save_dir = args.out_dir
        video_path = os.path.join(save_dir, video_id)
        video.download(video_path, filename='video')

        # TODO: Configure caption parametrization
        caption_lang = args.capt_lang
        try:
            caption = source.captions[caption_lang]
        except KeyError:
            raise ValueError(f'''No valid caption for video '{url}'.''')
        caption_srt = caption.generate_srt_captions()
        caption_path = os.path.join(save_dir, video_id, 'captions.txt')
        with open(caption_path, 'w') as file:
            file.write(caption_srt)





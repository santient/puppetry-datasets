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
        video.download(f'../{save_dir}/{video_id}', filename='video')

        # TODO: Make captions parametrized at the end
        caption_lang = 'en'
        try:
            caption = source.captions[caption_lang]
        except KeyError:
            raise ValueError(f'''No valid caption for video '{url}'.''')
        caption_srt = caption.generate_srt_captions()
        with open(f'../{save_dir}/{video_id}/captions.txt', 'w') as file:
            file.write(caption_srt)





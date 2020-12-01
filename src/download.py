import os
from pytube import YouTube


def download_videos(args):
    """
    Downloads the list of YouTube videos and accompanying English subtitles from
    provided URLs
    :param args: List of YouTube video URLs
    """
    for url in args:
        try:
            source = YouTube(url)
        except:
            raise ValueError(f''''{url}' is not a valid URL''')
        video = source.streams.get_highest_resolution()
        name = source.title
        video.download('../vids', filename=name)

        # TODO: Look into the caption types/codes in YouTube to get a
        #  comprehensive list of those that can be utilized.
        caption_lang = 'en'
        try:
            caption = source.captions[caption_lang]
        except KeyError:
            raise ValueError(f'''No valid caption for video '{url}'.''')
        caption_srt = caption.generate_srt_captions()
        with open(f'../vids/{name}.txt', 'w') as file:
            file.write(caption_srt)





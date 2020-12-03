import os
import re
import pytube


def download_videos(args):
    """
    Downloads the list of YouTube videos and accompanying English subtitles from
    provided URLs
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

        all_captions = [x.code for x in source.captions]
        if 'en' in all_captions:
            caption_lang = 'en'
        else:
            regex = re.compile('en-*')
            captions = list(filter(regex.match, all_captions))
            if captions:
                caption_lang = captions[0]  # arbitrarily picking the first
            else:
                raise ValueError(f'''No valid caption for video '{url}'.''')

        caption = source.captions[caption_lang]
        caption_srt = caption.generate_srt_captions()
        caption_path = os.path.join(save_dir, video_id, 'captions.txt')
        with open(caption_path, 'w') as file:
            file.write(caption_srt)





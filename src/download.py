import os
import re
import pytube
import subprocess


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
        lang = args.lang  # language of the caption as a code (e.g. en)
        if lang in all_captions:
            caption_lang = lang
        else:
            regex = re.compile(f'{lang}-.*')
            captions = list(filter(regex.match, all_captions))
            if captions:
                caption_lang = captions[0]  # arbitrarily picking the first
            else:
                raise ValueError(f'''No valid caption for video '{url}'.''')

        caption = source.captions[caption_lang]
        caption_srt = caption.generate_srt_captions()
        caption_path = os.path.join(save_dir, video_id, 'captions.srt')
        with open(caption_path, 'w') as file:
            file.write(caption_srt)

        txtgrid_path = os.path.join(save_dir, video_id, 'captions.TextGrid')
        cmd = f'python3 -m textgrid_convert -i {caption_path} -o {txtgrid_path}'
        subprocess.run(cmd.split())








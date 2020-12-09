import os
import pytube
import subprocess

def extract_frames(args):
    
    for url in args.url_file:
        try:
            video_id = pytube.extract.video_id(url)
        except: 
            raise ValueError(f'{url} is not a valid URL')
            
        # video path is created in download.py
        root_path = os.path.join(args.out_dir, video_id)
        video_path = os.path.join(root_path, 'video.mp4')
        
        # frame rate same as video
        cmds = ['ffmpeg','-i',f'{video_path}', f'{root_path}frame%d.jpg']
        ffmpeg = subprocess.run(cmds, stdout=subprocess.PIPE, text=True)

        # raises CalledProcessError if exit code not 0
        ffmpeg.check_returncode()

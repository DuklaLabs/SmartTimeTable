#!/usr/bin/env python3

import vlc
import time
from pathlib import Path

def play_video(video_name):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets" / "videos"

    media_player = vlc.MediaPlayer()
    media = vlc.Media(ASSETS_PATH / video_name)
    media_player.set_media(media)
    media_player.toggle_fullscreen()
    
    media_player.play()
    
    time.sleep(2)
    time.sleep(media_player.get_length()/1000)
    
    media_player.stop()

if __name__ == "__main__":
    play_video("SpinningFish.mp4")


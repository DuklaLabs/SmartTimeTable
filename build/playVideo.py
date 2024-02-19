import vlc
import time
  
media_player = vlc.MediaPlayer()
media = vlc.Media("C:\\Users\\Majrich\\Documents\\Code\\SmartTimeTable\\build\\assets\\videos\\SpinningFish.mp4")
media_player.set_media(media)
media_player.toggle_fullscreen()
  
media_player.play()
 
time.sleep(2)
time.sleep(media_player.get_length()/1000)

media_player.stop()


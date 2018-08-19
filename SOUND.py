from pygame import mixer
import SETTINGS

def play_sound(sound, distance):
    if distance <= SETTINGS.tile_size * SETTINGS.render:
        if distance >= SETTINGS.tile_size * (SETTINGS.render*0.8):
            mixer.Sound.set_volume(sound, 0.2 * SETTINGS.volume)

        elif distance >= SETTINGS.tile_size * (SETTINGS.render*0.4):
            mixer.Sound.set_volume(sound, 0.5 * SETTINGS.volume)

        else:
            mixer.Sound.set_volume(sound, SETTINGS.volume)

        mixer.Sound.play(sound)

import pygame

class SoundManager:
    """
    Manages all sound effects and background music for the game.
    """

    def __init__(self):
        """
        Initialize the SoundManager.
        """
        self.music_volume = 0.5
        self.sound_volume = 0.5
        self.sounds = {}

    def load_music(self, music_file):
        """
        Load background music.
        Args:
            music_file (str): Path to the music file.
        """
        pygame.mixer.music.load(music_file)

    def play_music(self, loops=-1):
        """
        Play the loaded background music.
        Args:
            loops (int): Number of times to loop the music. -1 means infinite loop.
        """
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loops)

    def stop_music(self):
        """
        Stop the background music.
        """
        print("stop music")
        pygame.mixer.music.stop()

    def is_music_playing(self):
        """
        Check if the background music is currently playing.
        Returns:
            bool: True if music is playing, False otherwise.
        """
        return pygame.mixer.music.get_busy()

    def load_sound(self, sound_name, sound_file):
        """
        Load a sound effect.
        Args:
            sound_name (str): Name to reference the sound.
            sound_file (str): Path to the sound file.
        """
        self.sounds[sound_name] = pygame.mixer.Sound(sound_file)

    def play_sound(self, sound_name):
        """
        Play a loaded sound effect.
        Args:
            sound_name (str): Name of the sound to play.
        """
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(self.sound_volume)
            self.sounds[sound_name].play()

    def set_music_volume(self, volume):
        """
        Set the volume for background music.
        Args:
            volume (float): Volume level (0.0 to 1.0).
        """
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def set_sound_volume(self, volume):
        """
        Set the volume for sound effects.
        Args:
            volume (float): Volume level (0.0 to 1.0).
        """
        self.sound_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)

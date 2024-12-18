# sound_manager.py
import pygame
from pathlib import Path
from typing import Dict, Optional
from config import SOUND_SETTINGS, SOUND_REGISTRY

class SoundManager:
    """
    Centralized sound management system for the entire game.
    Handles preloading, caching, and playing of all game sounds.
    """
    def __init__(self):
        """Initialize the sound manager with default settings and preload all game sounds."""
        self.music_volume = SOUND_SETTINGS['default_music_volume']
        self.sound_volume = SOUND_SETTINGS['default_sound_volume']
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.current_music: Optional[str] = None
        
        # Define sound categories and their associated files
        self.sound_registry = SOUND_REGISTRY
        
        # Preload all sounds on initialization
        self._preload_sounds()
    
    def _preload_sounds(self):
        """Preload all sound effects into memory."""
        sound_path = Path('assets/sound')
        for category in self.sound_registry.values():
            for sound_id, filename in category.items():
                try:
                    full_path = sound_path / filename
                    self.sounds[sound_id] = pygame.mixer.Sound(str(full_path))
                    self.sounds[sound_id].set_volume(self.sound_volume)
                except Exception as e:
                    print(f"Failed to load sound {sound_id} from {full_path}: {e}")

    def play_sound(self, sound_id: str) -> bool:
        """
        Play a sound effect by its ID.
        
        Args:
            sound_id: The identifier of the sound to play
            
        Returns:
            bool: True if sound played successfully, False otherwise
        """
        if sound_id in self.sounds:
            try:
                self.sounds[sound_id].play()
                return True
            except Exception as e:
                print(f"Failed to play sound {sound_id}: {e}")
                return False
        print(f"Sound {sound_id} not found in registry")
        return False

    def play_music(self, music_id: str, loops: int = -1):
        """
        Play background music by its ID.
        
        Args:
            music_id: The identifier of the music track to play
            loops: Number of times to loop (-1 for infinite)
        """
        if music_id == self.current_music:
            return  # Already playing this track
            
        try:
            music_file = self.sound_registry['music'].get(music_id)
            if music_file:
                full_path = Path('assets/sound') / music_file
                pygame.mixer.music.load(str(full_path))
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops)
                self.current_music = music_id
        except Exception as e:
            print(f"Failed to play music {music_id}: {e}")
        # I added a try-except here because as I was building the sound mananger I was having a lot of issues. TODO: remove print statement and try-except block

    def stop_music(self):
        """Stop the currently playing music track."""
        pygame.mixer.music.stop()
        self.current_music = None

    def set_music_volume(self, volume: float):
        """Set the volume for background music (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume: float):
        """Set the volume for sound effects (0.0 to 1.0)."""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)

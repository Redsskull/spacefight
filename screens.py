from .screens.main_menu import MainMenu
from .screens.story_screen import StoryScreen

__all__ = ['MainMenu', 'StoryScreen']

#This exists here to avoid circular imports. I am not sure it is the best way to do this, but I am learning as I go.
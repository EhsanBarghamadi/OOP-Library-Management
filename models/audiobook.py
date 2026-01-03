from models.book import Book, BookGenre
from enum import Enum

class BookAudioFormat(Enum):
    '''An enumeration of audio file formats used for book narrations.'''
    
    MP3 = "MPEG Layer III - High compatibility and compressed size."
    M4B = "MPEG-4 Audiobook - Supports chapters and bookmarks."
    WAV = "Waveform Audio - Uncompressed and high-quality format."
    AAC = "Advanced Audio Coding - Better sound quality than MP3."
    FLAC = "Free Lossless Audio Codec - High-fidelity without data loss."
    OGG = "Ogg Vorbis - Open-source alternative to MP3."

    @staticmethod
    def show_format():
        return [f.name for f in BookAudioFormat]

class AudioBook(Book):
    '''Represents an audiobook with time-based duration, narrator details, and audio format.'''

    def __init__(self, title : str, author : str, genre : BookGenre, hours : int, minutes : int, narrator : str, audio_format : BookAudioFormat, pages : int = 1):
        super().__init__(title, author, genre, pages)
        self.narrator = narrator
        self.audio_format = audio_format
        self._duration_seconds = (hours * 3600) + (minutes * 60)

    @property
    def hours(self):
        return self._duration_seconds // 3600
    
    @hours.setter
    def hours(self, value):
        current_minutes = (self._duration_seconds % 3600) // 60
        self._duration_seconds = (value * 3600) + (current_minutes * 60)

    @property
    def minutes(self):
        return (self._duration_seconds % 3600) // 60

    @minutes.setter
    def minutes(self, value):
        current_hours = self._duration_seconds // 3600
        self._duration_seconds = (current_hours * 3600) + (value * 60)

    @property
    def audio_format(self):
        return self._audio_format

    @audio_format.setter
    def audio_format(self, value):
        if isinstance(value, BookAudioFormat):
            self._audio_format = value
        else:
            raise TypeError("The entered format is not valid.")

    @property
    def duration_seconds(self):
        return self._duration_seconds

    @duration_seconds.setter
    def duration_seconds(self, value):
        if value <= 0:
            raise ValueError("Total duration must be positive!")
        else:
            self._duration_seconds = value

    def __str__(self):
        base_info = super().__str__()
        return (f"{base_info}\n"
                f"Narrator => {self.narrator}\n"
                f"Duration Book => {self.hours}h:{self.minutes}m\n"
                f"Audio format => {self.audio_format.name} ({self.audio_format.value})")
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "class_type": "AudioBook",
            "hours" : self.hours,
            "minutes" : self.minutes,
            "narrator": self.narrator,
            "audio_format": self.audio_format.name
        })
        return data
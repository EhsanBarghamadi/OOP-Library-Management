from datetime import datetime
from models.book import Book
from models.audiobook import AudioBook
from services.progress_manager import ProgressManager

class ReadingLog():
    """Manages reading sessions, progress tracking, and personal notes for a specific book."""

    def __init__(self, book : Book, progress_value : int) -> None:
        self.book = book
        self.progress_value = progress_value
        self.log_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self._note = []

    @property
    def progress_value(self):
        return self._progress_value

    @progress_value.setter
    def progress_value(self, value):
        if value < 0:
            raise ValueError("Progress value cannot be negative!")
        max_limit = self.book.duration_seconds if isinstance(self.book, AudioBook) else self.book.pages
        if value > max_limit:
            raise ValueError(f"Progress beyond the allowed ceiling! Max is {max_limit}")
        self._progress_value = value

        
    @property
    def progress(self) -> tuple[bool, tuple[str, str]]:
        if isinstance(self.book, AudioBook):
            total = self.book.duration_seconds
        else:
            total = self.book.pages
        percentage = ProgressManager.calculate_percentage(self.progress_value, total)
        if percentage > 0:
            return True, ProgressManager.generate_bar(percentage)
        else:
            return False, ("░It's not time to start.░", "0%")
            
    def add_note(self, text : str) -> None:
        _, result = self.progress
        bar_text, percen = result
        if text:
            note_entry = {
                "content": text,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "at_progress": self.progress_value,
                "visual_bar": bar_text + percen
            }
            self._note.append(note_entry)
        
    @property
    def note(self):
        return self._note if self._note else ["No notes recorded."]
    
    def to_dict(self):
        return {
            "book_title": self.book.title,
            "progress_value": self.progress_value,
            "log_date": self.log_date,
            "notes": self._note
        }

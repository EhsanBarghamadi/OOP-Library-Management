from models.book import Book, BookGenre
from models.ebook import EBook, EBookFormat
from models.audiobook import AudioBook, BookAudioFormat
from models.reading_log import ReadingLog

class ReadingTracker():
    """Orchestrates the book collection management and tracks user reading progress activities."""

    def __init__(self):
        self.list_logs = []
        self.list_books = []

    def add_book(self, title : str, author : str, genre : BookGenre, pages : int):
        if any(b.title == title for b in self.list_books):
            raise ValueError("This book is already registered in the library!")
        self.list_books.append(Book(title, author, genre, pages))
        return
    
    def add_ebook(self, title : str, author : str, genre : str, pages : int, file_size : int, file_format: EBookFormat):
        if any(b.title == title for b in self.list_books):
            raise ValueError("This book is already registered in the library!")
        self.list_books.append(EBook(title, author, genre, pages, file_size, file_format))
        return

    def add_audiobook(self, title: str, author: str, genre: BookGenre, hours: int, minutes: int, narrator: str, audio_format: BookAudioFormat, pages: int = 1):
        if any(b.title == title for b in self.list_books):
            raise ValueError("This book is already registered in the library!")
        self.list_books.append(AudioBook(title, author, genre, hours, minutes, narrator, audio_format, pages))
        return

    def find_book(self, name : str):
        search_name = name.strip().lower()
        for item in self.list_books:
            if item.title.lower() == search_name.lower():
                book_type = self.type_book(item)
                return item, book_type
        else:
            return None, "The desired book is not available in the library."
    
    @staticmethod
    def type_book(book : object):
        if isinstance(book, AudioBook):
            return "AudioBook"        
        elif isinstance(book, EBook):
            return "EBook"
        elif isinstance(book, Book):
            return "Book"
        
    def record_reading(self, book_name: str, progress: int, note: str = None):
        book_obj, message = self.find_book(book_name)
        if not book_obj:
            print(f"Error: {message}")
            return None
        for log in self.list_logs:
            if log.book == book_obj:
                log.progress_value = progress 
                if note:
                    log.add_note(note)
                print(f"Updated progress for {book_obj.title}.")
                return log
        new_log = ReadingLog(book_obj, progress)
        if note:
            new_log.add_note(note)
        self.list_logs.append(new_log)
        print(f"New reading session recorded for {book_obj.title}.")
        return new_log
    
    def stats_report(self):
        physical_books = []
        ebooks = []
        audiobooks = []      
        for item in self.list_books:
            if isinstance(item, AudioBook):
                audiobooks.append(item)
            elif isinstance(item, EBook):
                ebooks.append(item)
            elif isinstance(item, Book):
                physical_books.append(item)
        print("\n" + "═"*30)
        print("📊 LIBRARY STATISTICS REPORT")
        print("═"*30)
        print(f"📚 Physical Books: {len(physical_books)}")
        print(f"💻 E-Books:       {len(ebooks)}")
        print(f"🎧 Audio Books:    {len(audiobooks)}")
        print(f"✨ Total Assets:   {len(self.list_books)}")
        print("═"*30)       

    def my_dashboard(self):
            if not self.list_books:
                print("Your library is empty. Add some books to start your journey!")
                return
            print("\n" + "✨ YOUR READING JOURNEY ✨")
            print("═" * 30)
            for book in self.list_books:
                type_name = self.type_book(book)
                print(f"[{type_name}] {book.title}")
                log = next((l for l in self.list_logs if l.book == book), None)
                if log:
                    is_complete, (bar, percentage) = log.progress
                    print(f"  Progress: {percentage}%")
                    if log.note:
                        print("  📝 Notes:")
                        notes_list = log.note
                        if isinstance(notes_list, list) and notes_list != ["No notes recorded."]:
                            for entry in notes_list:
                                time = entry['timestamp']
                                content = entry['content']
                                v_bar = entry['visual_bar']
                                print(f"    └─ [{time}] {v_bar} -> {content}")
                else:
                    print(f"  Status: ░ Not started yet")
                print("-" * 30)
    
    def to_dict(self):
        return {
            "list_books": [book.to_dict() for book in self.list_books],
            "list_logs": [log.to_dict() for log in self.list_logs]
        }

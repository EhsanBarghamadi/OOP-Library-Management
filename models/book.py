from datetime import datetime
from enum import Enum

class BookGenre(Enum):
    '''An enumeration of literary genres with their formal descriptions.'''

    FICTION = "Literature in the form of prose that describes imaginary events and people."
    NON_FICTION = "Writing that is based on facts, real events, and real people."
    SCIENCE_FICTION = "Speculative fiction dealing with futuristic concepts like space travel."
    HISTORY = "Narratives about past events and chronological records of nations."
    BIOGRAPHY = "An account of someone's life written by someone else."
    MYSTERY = "Fiction involving a puzzling crime or a situation that needs to be solved."
    OTHER = "Books that do not fit into the standard predefined categories."

    @staticmethod
    def show_genre():
        return [f.name for f in BookGenre]

class Book():
    '''This class is used to model the basic information of the book.'''

    def __init__(self, title : str, author : str, genre : BookGenre, pages : int ) -> None:
        self.title = title
        self.author = author
        self.genre = genre
        self.pages = pages
        self.date_add = datetime.now()
    
    @property
    def genre(self):
        return self._genre
       
    @genre.setter
    def genre(self, value):
        if isinstance(value, BookGenre):
            self._genre = value
        else:
            raise TypeError("The entered genre is not valid!")

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, value):
        if value <= 0:
            raise ValueError("The number of pages must be a positive number.")
        else:
             self._pages = value
    
    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Author: {self.author}\n"
                f"Genre: {self.genre.name} ({self.genre.value})\n"
                f"Pages: {self.pages}\n"
                f"Date Added: {self.date_add.strftime('%Y-%m-%d %H:%M')}")
    
    def to_dict(self):
        return {
            "class_type": "Book",
            "title": self.title,
            "author": self.author,
            "genre": self.genre.name,
            "pages": self.pages,
            "date_add": self.date_add.strftime("%Y-%m-%d %H:%M")
        }
    

from models.book import Book, BookGenre
from enum import Enum 

class EBookFormat(Enum):
    '''Defines supported digital file formats and their full technical names.'''

    PDF = "Portable Document Format"
    EPUB = "Electronic Publication"
    MOBI = "Mobipocket"
    AZW3 = "Kindle Format"

    @staticmethod
    def show_format():
        return [f.name for f in EBookFormat]

class EBook(Book):
    ''' A specialized model representing digital books with file size and format attributes.'''

    def __init__(self, title : str, author : str, genre : BookGenre, pages : int, file_size : int, file_format: EBookFormat ):
        super().__init__(title, author, genre, pages)
        self.file_size = file_size
        self.file_format = file_format
        
    @property
    def file_size(self):
        return self._file_size

    @file_size.setter    
    def file_size(self, value):
        if value <= 0:
            raise ValueError("Size must be positive!")
        self._file_size = value

    @property
    def file_format(self):
        return self._file_format

    @file_format.setter
    def file_format(self, value):
        if isinstance(value, EBookFormat):
            self._file_format = value
        else:
            raise TypeError(f"The select format is not valid!")
 
    def __str__(self):
        base_info = super().__str__()
        return (f"{base_info}\n"
                f"Format: {self.file_format.name} ({self.file_format.value})\n"
                f"Size: {self.file_size}MB")
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "class_type": "EBook",
            "file_size": self.file_size,
            "file_format": self.file_format.name
        })
        return data

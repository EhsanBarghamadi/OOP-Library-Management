import json
from services.library_system import LibrarySystem
from models.book import Book, BookGenre
from models.ebook import EBook, EBookFormat
from models.audiobook import AudioBook, BookAudioFormat
from models.reading_log import ReadingLog

def save_data(library_system, file_path):
    """Saves the entire library system state to a JSON file."""
    try:
        data_to_save = library_system.to_dict()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4)
        print("✅ Data saved successfully!")
    except Exception as e:
        print(f"❌ Error during saving: {e}")

def load_data(file_path):
    """Loads the library system state from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        system = LibrarySystem()

        for u_data in raw_data.get("users", []):
            system.add_user(u_data['username'], u_data['password'])
            current_user = system.user_list[-1]

            # Load Books
            for b_data in u_data['tracker'].get('list_books', []):
                try:
                    genre_enum = BookGenre[b_data['genre']]
                    book_class = b_data.get('class_type', 'Book')

                    if book_class == "Book":
                        current_user.tracker.add_book(b_data['title'], b_data['author'], genre_enum, b_data['pages'])
                    elif book_class == "EBook":
                        format_enum = EBookFormat[b_data['file_format']]
                        current_user.tracker.add_ebook(b_data['title'], b_data['author'], genre_enum, b_data['pages'], b_data['file_size'], format_enum)
                    elif book_class == "AudioBook":
                        format_enum = BookAudioFormat[b_data["audio_format"]]
                        current_user.tracker.add_audiobook(
                            title=b_data['title'],
                            author=b_data['author'],
                            genre=genre_enum,
                            hours=b_data['hours'],
                            minutes=b_data['minutes'],
                            narrator=b_data['narrator'],
                            audio_format=format_enum,
                            pages=b_data.get('pages', 1)
                        )
                        if 'duration_seconds' in b_data:
                            current_user.tracker.list_books[-1].duration_seconds = b_data['duration_seconds']

                except (KeyError, ValueError) as e:
                    print(f"⚠️ Warning: Could not load book '{b_data.get('title', 'Unknown')}'. Error: {e}")
                    continue

            # Load Reading Logs and Notes
            if 'list_logs' in u_data.get('tracker', {}):
                for l_data in u_data['tracker']['list_logs']:
                    book_title = l_data.get('book_title')
                    if not book_title:
                        continue
                    book_obj = next((b for b in current_user.tracker.list_books if b.title == book_title), None)
                    if not book_obj:
                        print(f"⚠️ Warning: Book '{book_title}' for a reading log not found. Skipping log.")
                        continue
                    log = ReadingLog(book_obj, l_data['progress_value'])
                    log.log_date = l_data.get('log_date', log.log_date)
                    saved_notes = l_data.get('notes', [])
                    if saved_notes and saved_notes != ["No notes recorded."]:
                        log._note = saved_notes
                    current_user.tracker.list_logs.append(log)

        print("✅ Data loaded successfully!")
        return system

    except FileNotFoundError:
        print("📁 Database file not found. Creating a new one...")
        new_system = LibrarySystem()
        save_data(new_system, file_path)
        return new_system
    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Error parsing database file: {e}. Starting with a fresh database.")
        return LibrarySystem()
    except Exception as e:
        print(f"❌ An unexpected error occurred during loading: {e}. Starting fresh.")
        return LibrarySystem()

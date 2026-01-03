import json
from storage.json_handler import save_data, load_data
from services.library_system import LibrarySystem
from security_auth import get_username, get_password, get_birthdate, check_password_user
from getpass import getpass
from datetime import datetime
from models.book import Book, BookGenre
from models.ebook import EBook, EBookFormat
from models.audiobook import AudioBook, BookAudioFormat

def get_enum_input(enum_class, prompt):
    print(f"Available: {[e.name for e in enum_class]}")
    while True:
        choice = input(prompt).upper().strip()
        try:
            return enum_class[choice]
        except KeyError:
            print(f"❌ '{choice}' is not valid. Try again.")
            input("Please press enter...")

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Invalid input. Please enter number.")

def main():
    DATABASE = "library_db.json"
    system = load_data(DATABASE)
    
    while True:
        print("\n--- 📚 Welcome to Personal Reading Tracker ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Select an option: ")
        
        match choice:

            # New user registration
            case "1":
                print("\n--- 📝 User Registration ---")
                username = get_username()
                if any(u.username == username for u in system.user_list):
                    print("❌ Username already exists!")
                    input("Please press enter...")
                    continue
                password = get_password()
                birth_date = get_birthdate()
                birth_year = birth_date[0]
                final_score, filters = check_password_user(username, password, birth_year)
                print("=" * 20)
                for index, item in enumerate(filters, start=1):
                    print(f"{index}  {item}")
                print(f"\n⭐ Password Score: {final_score}/9")
                print("=" * 20)
                if final_score < 6:
                    print(f"❌ Password is too weak (Score: {final_score}/9)")
                    input("Please press enter...")
                    continue
                system.add_user(username, password)
                print(f"✅ User '{username}' registered successfully with score {final_score}!")
                save_data(system, DATABASE)
                input("Please press enter...")
                continue
            # User login
            case "2":
                print("\n--- 🔑 Login ---")
                username = input("Username: ")
                password = getpass("Password: ")
                success, message, user = system.login(username, password)
                if success:
                    print(f"✨ Welcome back, {username}!")
                    while True:
                        print(f"\n--- 👤 {user.username}'S DASHBOARD ---")
                        print("1. Add Book")
                        print("2. Update Progress")
                        print("3. View My Stats")
                        print("4. Logout")

                        sub_choice = input("Action: ")

                        match sub_choice:

                            # Add new book
                            case "1":
                                title = input("Title: ")
                                author = input("Author: ")
                                genre = get_enum_input(BookGenre, "Select Genre: ")
                                print("\nSelect Book Type: (1) Physical, (2) E-Book, (3) AudioBook")
                                while True:
                                    book_type = input("Choice number: ")
                                    # Physical book
                                    if book_type == "1":
                                        pages = get_int_input("Total Pages: ")
                                        user.tracker.add_book(title, author, genre, pages)
                                        print("✅ New book added successfully.")
                                        save_data(system, DATABASE)
                                        input("Press Enter to return to menu...")
                                        break         
                                    # Electronic book
                                    elif book_type == "2":
                                        pages = get_int_input("Total Pages: ")
                                        size = get_int_input("Size (MB): ")
                                        f_type = get_enum_input(EBookFormat, "Format (PDF/EPUB): ")
                                        user.tracker.add_ebook(title, author, genre, pages, size, f_type)
                                        print("✅ New book added successfully.")
                                        save_data(system, DATABASE)
                                        input("Press Enter to return to menu...")
                                        break
                                    # Audio Book
                                    elif book_type == "3":
                                        hours = get_int_input("Duration (Hours): ")
                                        minutes = get_int_input("Duration (Minutes): ")
                                        while True:
                                            narrator = input("Narrator: ")
                                            if narrator:
                                                break
                                            print("❌ The narrator name cannot be empty.")
                                            input("Press Enter to try again...")
                                            continue
                                        f_type = get_enum_input(BookAudioFormat, "Format (MP3/WAV): ")
                                        user.tracker.add_audiobook(title, author, genre, hours, minutes, narrator, f_type, 1)
                                        print("✅ New book added successfully.")
                                        save_data(system, DATABASE)
                                        input("Press Enter to return to menu...")
                                        break
                                    else:
                                        print("The selected type is not correct")
                                        input("Please press enter...")
                                        continue
                            # Study progress record
                            case "2":
                                if not user.tracker.list_books:
                                    print("❌ No books to update!")
                                    input("Please press enter...")
                                    continue
                                print("\n--- 📚 Your Books List ---")
                                for i, b in enumerate(user.tracker.list_books, start=1):
                                    target_log = None
                                    for log in user.tracker.list_logs:
                                        if log.book.title == b.title:
                                            target_log = log
                                            break
                                    if target_log:
                                        _, (_, percentage) = target_log.progress 
                                        print(f"{i}. {b.title} ({percentage})")
                                    else:
                                        print(f"{i}. {b.title} (0%)")
                                while True:
                                    choice_idx = get_int_input("\nSelect book number to update (or 0 to cancel): ")
                                    if choice_idx == 0: break
                                    
                                    if 1 <= choice_idx <= len(user.tracker.list_books):
                                        target_book = user.tracker.list_books[choice_idx - 1]
                                        while True:
                                            if isinstance(target_book, AudioBook):
                                                new_progress = get_int_input(f"Enter your progress in minutes for '{target_book.title}': ")
                                                new_progress *= 60
                                            else:
                                                new_progress = get_int_input(f"Enter current progress for '{target_book.title}': ")
                                            note = input("Daily note (press enter to skip): ").strip()
                                            try:
                                                log_obj = user.tracker.record_reading(target_book.title, new_progress)
                                                if note:
                                                    log_obj.add_note(note)
                                                
                                                print("✅ Progress updated successfully!")
                                                save_data(system, DATABASE)
                                                input("Please press enter...")
                                                break
                                            except Exception as e:
                                                print(f"❌ Error: {e}")
                                                
                                                if input("Try again? (y/n): ").lower() != 'y':
                                                    break
                                        break 
                                    else:
                                        print(f"❌ Invalid number! (1-{len(user.tracker.list_books)})")
                            # View dashboard
                            case "3":
                                user.tracker.my_dashboard()
                            # Return to menu...
                            case "4":
                                input("Press Enter to return to menu...")
                                break
                else:
                    print("❌ Invalid username or password.")
                    input("Please press enter...")
                    continue
            case "3":
                save_data(system, "library_db.json")
                print("👋 Goodbye!")
                break
            
            case _:
                print("⚠️ Invalid choice. Please try again.")
                input("Press Enter to return to menu...")

if __name__ == "__main__":
    main()
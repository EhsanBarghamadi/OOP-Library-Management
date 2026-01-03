from services.reading_tracker import ReadingTracker

class User():
    """Represents a system user, encapsulating credentials and their personal reading tracker."""

    def __init__(self, username, password, tracker : object):
        self.username = username
        self.password = password
        self.tracker = tracker

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "tracker": self.tracker.to_dict()
        }
    
class LibrarySystem:
    """Acts as the central controller for managing user registration, authentication, and global data."""

    def __init__(self):
        self.user_list = []
    
    def add_user(self, username , password) -> tuple[ bool , str , object]:
        if any(user.username == username for user in self.user_list):
            return False, f"❌ Error: User '{username}' already exists!"
        new_user = User(username, password, ReadingTracker())
        self.user_list.append(new_user)
        return True , f"✅ User '{username}' added successfully."
    
    def login(self, username, password) -> tuple[ bool , str ]:
        for item in self.user_list:
            if item.username == username:
                if item.password == password:
                    return True, f"✅ '{username}' has successfully logged in.", item
                else:
                    return False, "❌ Your password is incorrect.", None
        return False, "❌ Your username was not found.", None
    
    def to_dict(self):
        return {
            "users": [user.to_dict() for user in self.user_list]
        }
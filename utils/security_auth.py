from getpass import getpass
from datetime import datetime

# get username & check not empty
def get_username(): 
    while True:
        username = input("Please enter your username: ")
        if username.strip() == "":
            print("⚠️  Username cannot be empty. Please try again (。_。)")
        else:
            return username.strip()
    
# get password & check not emptyٍ
def get_password():
    while True:
        password = getpass("Please enter your password: ")
        if password.strip() == "":
            print("⚠️  Password cannot be empty. Please try again (。_。)")
        else:
            return password.strip()
        
# get birthdate
def get_birthdate():
    DATE_FORMAT = "%Y/%m/%d"

    while True:
        birthdate_str = input(f"Please enter your birthdate (YYYY/MM/DD): ").strip()
        if not birthdate_str:
            print("⚠️   Birthdate cannot be empty ( . _ .)")
            continue
        try:
            datetime.strptime(birthdate_str, DATE_FORMAT)
            year, month, day = birthdate_str.split('/')
            return year, month, day
        except ValueError:
                print("❌  Invalid date format. Please use the exact format (YYYY/MM/DD).")

# Check 9 Filters for password
def check_password_user(username, password, birth_year):
    final_score = 9
    filter_text = []
    password_no_space = password.replace(" ", "")

# Filter 1 : Check for length password
    if len(password_no_space) > 8 :
        filter_text.append("✅   Password length is sufficient")
    else:
        final_score -= 1
        filter_text.append("❌   Password is shorter than 8 characters")

# Filter 2 : Check for contains any alpha in password
    is_alpha_list = []
    for char in password:
        is_alpha_list.append(char.isalpha())

    if True in is_alpha_list:
        filter_text.append("✅   Contains at least one English letter.")
    else:
        final_score -= 1
        filter_text.append("❌   Password does not contain any English letters.")
    
# Filter 3 : Check for contains any special character in password
    is_special_list = []

    for char in password_no_space:
        is_special_list.append(not char.isalpha() and not char.isdigit())

    if True in is_special_list:
        filter_text.append("✅   Contains at least one special character.")
    else:
        final_score -= 1
        filter_text.append("❌   Password does not contain any special characters.")

# Filter 4 : Check for contains any uppercase in password
    is_uppercase_list = []

    for char in password:
        is_uppercase_list.append(char.isupper())

    if True in is_uppercase_list:
        filter_text.append("✅   Contains at least one uppercase letter.")
    else:
        final_score -= 1 
        filter_text.append("❌   Password does not contain any uppercase letters.")

# Filter 5 : Check password for identical to the username
    if password_no_space != username:
        filter_text.append("✅   Password is not identical to the username.")
    else:
        final_score -= 1
        filter_text.append("❌   Password is identical to the username.")
# Filter 6 : Check password for swapcase username
    if password_no_space.swapcase() != username:
        filter_text.append("✅   Password is not the swapcase version of the username")
    else:
        final_score -= 1
        filter_text.append("❌   Password is the swapcase version of the username")
    
# Filter 7 : Check password special-character version of the username
    dict_leetspeak = {
    "@": "a", 
    "!": "i", 
    "$": "s",
    "4": "a", 
    "3": "e", 
    "0": "o", 
    "|": "l", 
    "l": "l", 
    "5": "s",
    "z": "s", 
    "2": "z", 
    "8": "b",
    "+": "t", 
    "7": "t",
    "9": "g", 
    "%": "x",
    "#": "h",
    "(": "c"
}
    leet_password = ""
    char_use = []
    alpha_replace = []
    full_item = []
    for char in password_no_space.lower():
        if char in dict_leetspeak:
            char_use.append(char)
            alpha_replace.append(dict_leetspeak[char])
            leet_password += dict_leetspeak[char]
        else:
            leet_password += char

    if leet_password != username.lower():
        filter_text.append("✅   Password is not a special-character version of the username.")
    else:
        final_score -= 1
        list_char_alpha = list(zip(char_use, alpha_replace))
        for item1, item2 in list_char_alpha:
            full_item.append(f"{item2} => {item1}")
        final_full_atem = ", ".join(full_item)
        filter_text.append(f"❌   Password is a special-character version of the username ({final_full_atem})")

# Filter 8 : Check for common password
    common_passwords = [
    "password", "123456", "12345678", "123456789", "qwerty", "12345", 
    "1234", "111111", "000000", "default", "admin", "usuario", 
    "welcome", "testing", "secret", "iloveyou", "access", "qazwsx", 
    "changeit", "master", "sistema", "mypassword", "masterkey", 
    "company", "project", "p@ssword","zxcvbnm","p@s$w0rd"
    ]
    if password_no_space.lower() not in common_passwords:
        filter_text.append("✅   Not a common password.")
    else:
        final_score -= 1
        filter_text.append("❌   Password is one of the most common passwords.")

# Filter 9 : Check birthdate in password
    if birth_year not in  password_no_space:
        filter_text.append("✅   Password does not contain the full birth year (YYYY).")
    else:
        final_score -= 1
        filter_text.append("❌   Password contains the full birth year (YYYY).")





    return final_score, filter_text

def descriptive_score_tip(final_score):
    if final_score < 4 :
        tip = "📌   Tip: Your password is too simple and easy to guess. Use a mix of letters, numbers, and symbols."
        pass_level = "Very weak"
        return tip, pass_level
    elif final_score < 8:
        tip = "📌   Tip: Your password is good, but increasing its length or variety of characters can make it even stronger."
        pass_level = "Medium"
        return tip, pass_level
    else:
        tip = "🎉   Congratulations! Your password is highly secure and passed all security checks. "
        pass_level = "Strong"
        return tip, pass_level
    


def main():
    USERNAME = get_username()
    PASSWORD = get_password()
    YEAR, MONTH, DAY = get_birthdate()
    final_score, filter_text = check_password_user(USERNAME,PASSWORD,YEAR)
    tip, des_score = descriptive_score_tip(final_score)
    print(f"Username: {USERNAME}")
    print(f"Password: {PASSWORD}")
    print()
    print("✅   Filter checks: ")   
    for item in filter_text:
        print(item)
    print()
    print(f"🔐 Final Score: {final_score} out of 9" )
    print(f"🔒 Security Level: {des_score}")
    print(tip)


if __name__ == "__main__":
    main()
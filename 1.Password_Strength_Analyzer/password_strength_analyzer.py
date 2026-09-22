import re
def check_password_strength(password):
    score = 0
    feedback = []

    # 1. Check Length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("• Make your password at least 8 to 12 characters long.")

    # 2. Check for Uppercase letters
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("• Add at least one uppercase letter (A-Z).")

    # 3. Check for Lowercase letters
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("• Add at least one lowercase letter (a-z).")

    # 4. Check for Numbers
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("• Add at least one number (0-9).")

    # 5. Check for Special Characters
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("• Add at least one special character (e.g., !, @, #, $).")

    # Determine strength rating
    if score >= 5:
        rating = "Strong 🟢"
    elif score >= 3:
        rating = "Moderate 🟡"
    else:
        rating = "Weak 🔴"

    return rating, feedback

# --- Interactive Test ---
if __name__ == "__main__":
    user_pass = input("Enter a password to test: ")
    rating, suggestions = check_password_strength(user_pass)

    print(f"\nPassword Strength: {rating}")
    if suggestions:
        print("Suggestions for improvement:")
        for note in suggestions:
            print(note)
    input("Press Enter to exit...")
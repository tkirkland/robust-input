#!/usr/bin/env python3
"""Complete user registration system example demonstrating robust_input features."""

import robust_input as ri

def main():
    print("🎯 User Registration System")
    print("=" * 40)
    
    # User information
    name = ri.get_input(
        prompt="👤 Full Name",
        min_length=2,
        max_length=50,
        allow_empty=False,
        prompt_style=[ri.InputStyle.BLUE, ri.InputStyle.BOLD],
        error_message="❌ Name must be 2-50 characters"
    )
    
    email = ri.get_input(
        prompt="📧 Email Address",
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        prompt_style=[ri.InputStyle.BLUE, ri.InputStyle.BOLD],
        error_message="❌ Please enter a valid email address"
    )
    
    age = ri.get_integer(
        prompt="🎂 Age",
        min_value=13,
        max_value=120,
        prompt_style=[ri.InputStyle.BLUE, ri.InputStyle.BOLD],
        error_message="❌ Age must be between 13 and 120"
    )
    
    password = ri.get_password(
        prompt="🔒 Password",
        min_length=8,
        pattern=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$',
        error_message="❌ Password must be 8+ chars with letters and numbers"
    )
    
    # Preferences
    theme = ri.get_choice(
        prompt="🎨 Theme Preference",
        choices=["light", "dark", "auto"],
        default="auto",
        prompt_style=[ri.InputStyle.BLUE, ri.InputStyle.BOLD]
    )
    
    # Summary
    print("\n✅ Registration Complete!")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Age: {age}")
    print(f"Theme: {theme}")
    print(f"Password: {'*' * len(password)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Registration cancelled.")
# Robust Input Module

A comprehensive and robust input routine for command-line applications in Python. This module provides a highly configurable input function with advanced terminal control, validation, and user experience features.

## Features

### Core Input Capabilities
- **Real-time Character Input**: Character-by-character processing with immediate feedback
- **Cursor Movement**: Full left/right arrow key support for in-place editing
- **Backspace Support**: Delete characters with proper cursor positioning
- **Default Values**: Built-in default value handling with validation
- **Cross-platform**: Works in both terminal and non-terminal environments

### Advanced Validation System
- **Length Validation**: Minimum and maximum length constraints
- **Type Validation**: Automatic casting to int, float, bool, str, and custom types
- **Pattern Validation**: Regular expression pattern matching
- **Choice Validation**: Selection from predefined options
- **Custom Validators**: User-defined validation functions
- **Composite Validation**: Multiple validation layers applied sequentially

### Professional User Experience
- **Smart Error Display**: Errors appear below input line without scrolling
- **Persistent Error Messages**: Errors stay visible until next validation
- **Instant Feedback**: No artificial delays - immediate validation response
- **Screen Real Estate Reuse**: Cursor repositioning prevents screen clutter
- **Clean Terminal Management**: Proper terminal state restoration

### Security & Styling
- **Password Masking**: Secure input with asterisk masking
- **ANSI Styling**: Full color and text style support
- **Customizable Messages**: User-defined prompts and error messages
- **Graceful Degradation**: Fallback behavior for non-terminal environments

## Requirements

- Python 3.6+
- Linux/Unix environment (uses `termios` and `tty` modules)
- Standard library only (no external dependencies)

## Installation

Simply copy the `robust_input.py` file to your project directory.

## Usage

### Basic Examples

```python
import robust_input as ri

# Simple string input
name = ri.get_input(prompt="Enter your name")
print(f"Hello, {name}!")

# Integer input with validation
age = ri.get_input(
    prompt="Enter your age",
    target_type=int,
    min_length=1,
    max_length=3,
    custom_validator=lambda x: 1 <= int(x) <= 120,
    error_message="Age must be between 1 and 120"
)

# String input with length constraints
username = ri.get_input(
    prompt="Choose a username",
    min_length=3,
    max_length=20,
    allow_empty=False,
    error_message="Username must be 3-20 characters"
)

# Choice selection
color = ri.get_input(
    prompt="Select your favorite color",
    choices=["red", "green", "blue", "yellow"],
    default="blue",
    error_message="Please choose from the available colors"
)
```

### Password and Security

```python
import robust_input as ri

# Password input with masking
password = ri.get_password(
    prompt="Enter your password",
    min_length=8,
    pattern=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
    error_message="Password must be at least 8 characters with letters and numbers"
)

# Secure input with custom validation
def strong_password(pwd: str) -> bool:
    return (len(pwd) >= 8 and 
            any(c.isupper() for c in pwd) and 
            any(c.islower() for c in pwd) and 
            any(c.isdigit() for c in pwd))

secure_pwd = ri.get_input(
    prompt="Create a strong password",
    is_password=True,
    custom_validator=strong_password,
    error_message="Password must have uppercase, lowercase, and numbers"
)
```

### Advanced Validation

```python
import robust_input as ri
import re

# Email validation
email = ri.get_input(
    prompt="Enter your email",
    pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    error_message="Please enter a valid email address"
)

# Custom validation function
def is_prime(value: str) -> bool:
    try:
        n = int(value)
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    except ValueError:
        return False

prime_number = ri.get_input(
    prompt="Enter a prime number",
    target_type=int,
    custom_validator=is_prime,
    error_message="Please enter a prime number"
)

# Multiple validation layers
user_id = ri.get_input(
    prompt="Enter user ID",
    target_type=int,
    min_length=1,
    max_length=10,
    custom_validator=lambda x: int(x) > 0,
    error_message="User ID must be a positive integer"
)
```

### Styling and Appearance

```python
import robust_input as ri

# Styled prompts and errors
styled_input = ri.get_input(
    prompt="Enter something special",
    prompt_style=[ri.InputStyle.BLUE, ri.InputStyle.BOLD],
    input_style=[ri.InputStyle.CYAN],
    error_style=[ri.InputStyle.RED, ri.InputStyle.BOLD],
    error_message="❌ Invalid input! Please try again."
)

# Colorful interactive menu
menu_choice = ri.get_input(
    prompt="🎮 Choose your action",
    choices=["start", "quit", "help"],
    default="start",
    prompt_style=[ri.InputStyle.GREEN, ri.InputStyle.BOLD],
    input_style=[ri.InputStyle.YELLOW],
    error_message="⚠️ Please choose 'start', 'quit', or 'help'"
)
```

### Convenience Functions

```python
import robust_input as ri

# Integer input with range validation
age = ri.get_integer(
    prompt="Enter your age",
    min_value=1,
    max_value=120,
    error_message="Age must be between 1 and 120"
)

# Choice from predefined options
color = ri.get_choice(
    prompt="Select your favorite color",
    choices=["red", "green", "blue", "yellow"],
    default="blue"
)

# IP address validation
ip_address = ri.get_ip_address(
    prompt="Enter server IP",
    default="192.168.1.1"
)

# Password with built-in masking
password = ri.get_password(
    prompt="Enter password",
    min_length=8,
    error_message="Password must be at least 8 characters"
)
```

### Error Handling and User Experience

```python
import robust_input as ri

# The input function handles all error display and cursor positioning
try:
    # This will show errors below the input line, then reposition cursor
    number = ri.get_input(
        prompt="Enter an even number",
        target_type=int,
        custom_validator=lambda x: int(x) % 2 == 0,
        error_message="❌ Must be an even number!",
        allow_empty=False
    )
    print(f"✅ You entered: {number}")
    
except KeyboardInterrupt:
    print("\n👋 Goodbye!")
except Exception as e:
    print(f"❌ An error occurred: {e}")
```

## API Reference

### Main Function

#### `get_input(prompt, **kwargs) -> Any`

The primary function for collecting user input with comprehensive validation and styling.

**Parameters:**
- `prompt` (str): The prompt text to display to the user
- `default` (Optional[str]): Default value if user presses Enter without input
- `min_length` (Optional[int]): Minimum required length for input
- `max_length` (Optional[int]): Maximum allowed length for input
- `allow_empty` (bool): Whether to allow empty input (default: True)
- `target_type` (Type): Type to cast the input to (default: str)
- `pattern` (Optional[str]): Regular expression pattern for validation
- `choices` (Optional[List[str]]): List of allowed input values
- `is_password` (bool): Whether to mask input with asterisks (default: False)
- `prompt_style` (Optional[List[str]]): ANSI styles for the prompt
- `input_style` (Optional[List[str]]): ANSI styles for user input
- `error_message` (Optional[str]): Custom error message for validation failures
- `error_style` (Optional[List[str]]): ANSI styles for error messages
- `custom_validator` (Optional[Callable[[str], bool]]): Custom validation function

**Returns:** The validated and type-cast input value

**Raises:** 
- `ValueError`: When validation fails (including default values)
- `KeyboardInterrupt`: When user presses Ctrl+C

### Convenience Functions

#### `get_password(prompt, **kwargs) -> str`
Collects password input with asterisk masking.

#### `get_integer(prompt, min_value=None, max_value=None, **kwargs) -> int`
Collects integer input with optional range validation.

#### `get_choice(prompt, choices, **kwargs) -> str`
Collects input from a predefined list of choices.

#### `get_ip_address(prompt, **kwargs) -> str`
Collects and validates IPv4 address input.

### Styling Classes

#### `InputStyle`
Provides ANSI color codes and text styles:

```python
# Colors
InputStyle.BLACK, InputStyle.RED, InputStyle.GREEN, InputStyle.YELLOW
InputStyle.BLUE, InputStyle.MAGENTA, InputStyle.CYAN, InputStyle.WHITE

# Text Styles
InputStyle.BOLD, InputStyle.UNDERLINE, InputStyle.RESET
```

#### `InputValidator`
Static methods for validation:
- `validate_length(value, min_len, max_len) -> bool`
- `validate_type(value, target_type) -> bool`
- `validate_pattern(value, pattern) -> bool`
- `validate_ip_address(value) -> bool`
- `validate_in_choices(value, choices) -> bool`

### Architecture

The module uses a clean architecture with separated concerns:

- **`InputHandler`**: Manages terminal interaction and character processing
- **`InputConfig`**: Encapsulates all configuration parameters
- **`InputValidator`**: Handles all validation logic
- **`InputStyle`**: Provides styling capabilities

## User Experience Features

### Smart Error Display
- Errors appear below the input line
- Error messages persist until next validation
- No screen scrolling or clutter
- Instant feedback without delays

### Terminal Control
- Character-by-character input processing
- Full cursor movement support (left/right arrows)
- Proper backspace handling
- Terminal state restoration

### Cross-Platform Support
- **Terminal mode**: Full features with ANSI escape sequences
- **Non-terminal mode**: Graceful fallback using standard `input()`
- **Automatic detection**: Seamlessly switches between modes

## Complete Example

```python
#!/usr/bin/env python3
"""Complete example demonstrating robust_input features."""

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
```

## Development

### Architecture Highlights
- **Low Cognitive Complexity**: Refactored from 700% complexity to manageable levels
- **Separated Concerns**: Each class handles a specific responsibility
- **Comprehensive Testing**: Extensive validation and error handling
- **Professional UX**: Terminal-grade user experience

### Code Quality
- Type hints throughout
- Comprehensive docstrings
- Clean error handling
- Proper resource management
- Cross-platform compatibility

## License

This project is open source and available under the [MIT License](LICENSE).
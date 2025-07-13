# API Reference

## Overview

The `robust_input` module provides a comprehensive input system for command-line applications with advanced validation, styling, and terminal control capabilities.

## Core Functions

### `get_input(prompt, **kwargs) -> Any`

Primary function for collecting user input with comprehensive validation and styling.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | **Required** | The prompt text to display to the user |
| `default` | `Optional[str]` | `None` | Default value if user presses Enter without input |
| `min_length` | `Optional[int]` | `None` | Minimum required length for input |
| `max_length` | `Optional[int]` | `None` | Maximum allowed length for input |
| `allow_empty` | `bool` | `True` | Whether to allow empty input |
| `target_type` | `Type` | `str` | Type to cast the input to (str, int, float, bool, or custom) |
| `pattern` | `Optional[str]` | `None` | Regular expression pattern for validation |
| `choices` | `Optional[List[str]]` | `None` | List of allowed input values |
| `is_password` | `bool` | `False` | Whether to mask input with asterisks |
| `prompt_style` | `Optional[List[str]]` | `None` | ANSI styles for the prompt |
| `input_style` | `Optional[List[str]]` | `None` | ANSI styles for user input |
| `error_message` | `Optional[str]` | `None` | Custom error message for validation failures |
| `error_style` | `Optional[List[str]]` | `None` | ANSI styles for error messages |
| `custom_validator` | `Optional[Callable[[str], bool]]` | `None` | Custom validation function |

**Returns:** The validated and type-cast input value

**Raises:**
- `ValueError`: When validation fails (including default values)
- `KeyboardInterrupt`: When user presses Ctrl+C

**Example:**
```python
import robust_input as ri

# Basic string input
name = ri.get_input("Enter your name")

# Integer with validation
age = ri.get_input(
    prompt="Enter your age",
    target_type=int,
    min_length=1,
    max_length=3,
    custom_validator=lambda x: 1 <= int(x) <= 120,
    error_message="Age must be between 1 and 120"
)

# Choice selection with styling
color = ri.get_input(
    prompt="Select your favorite color",
    choices=["red", "green", "blue", "yellow"],
    default="blue",
    prompt_style=[ri.InputStyle.CYAN, ri.InputStyle.BOLD],
    error_message="Please choose from the available colors"
)
```

## Convenience Functions

### `get_password(prompt, **kwargs) -> str`

Specialized function for password input with masking.

**Parameters:**
- `prompt` (str): The prompt to display
- `min_length` (Optional[int]): Minimum password length
- `max_length` (Optional[int]): Maximum password length
- `allow_empty` (bool): Whether to allow empty password (default: False)
- `pattern` (Optional[str]): Regex pattern for password validation
- `prompt_style` (Optional[List[str]]): ANSI styles for prompt
- `error_message` (Optional[str]): Custom error message
- `custom_validator` (Optional[Callable[[str], bool]]): Custom validation function

**Returns:** The validated password string

**Example:**
```python
password = ri.get_password(
    prompt="Enter your password",
    min_length=8,
    pattern=r'^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d@$!%*?&]{8,}$',
    error_message="Password must be at least 8 characters with letters and numbers"
)
```

### `get_integer(prompt, **kwargs) -> int`

Specialized function for integer input with range validation.

**Parameters:**
- `prompt` (str): The prompt to display
- `default` (Optional[int]): Default value
- `min_value` (Optional[int]): Minimum allowed value (inclusive)
- `max_value` (Optional[int]): Maximum allowed value (inclusive)
- `allow_empty` (bool): Whether to allow empty input (default: False)
- `prompt_style` (Optional[List[str]]): ANSI styles for prompt
- `input_style` (Optional[List[str]]): ANSI styles for input
- `error_message` (Optional[str]): Custom error message

**Returns:** The validated integer value

**Example:**
```python
age = ri.get_integer(
    prompt="Enter your age",
    min_value=13,
    max_value=120,
    error_message="Age must be between 13 and 120"
)
```

### `get_choice(prompt, choices, **kwargs) -> str`

Specialized function for choice selection from predefined options.

**Parameters:**
- `prompt` (str): The prompt to display
- `choices` (List[str]): List of allowed values
- `default` (Optional[str]): Default value
- `allow_empty` (bool): Whether to allow empty input (default: False)
- `prompt_style` (Optional[List[str]]): ANSI styles for prompt
- `input_style` (Optional[List[str]]): ANSI styles for input
- `error_message` (Optional[str]): Custom error message

**Returns:** The selected choice

**Example:**
```python
theme = ri.get_choice(
    prompt="Choose your theme",
    choices=["light", "dark", "auto"],
    default="auto"
)
```

### `get_ip_address(prompt, **kwargs) -> str`

Specialized function for IPv4 address input with validation.

**Parameters:**
- `prompt` (str): The prompt to display
- `default` (Optional[str]): Default IP address
- `allow_empty` (bool): Whether to allow empty input (default: False)
- `prompt_style` (Optional[List[str]]): ANSI styles for prompt
- `input_style` (Optional[List[str]]): ANSI styles for input
- `error_message` (Optional[str]): Custom error message

**Returns:** The validated IP address

**Example:**
```python
server_ip = ri.get_ip_address(
    prompt="Enter server IP address",
    default="192.168.1.1"
)
```

## Core Classes

### `InputStyle`

Provides ANSI escape codes and styling utilities.

#### Color Constants

**Foreground Colors:**
- `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, `WHITE`
- `BRIGHT_BLACK`, `BRIGHT_RED`, `BRIGHT_GREEN`, `BRIGHT_YELLOW`, `BRIGHT_BLUE`, `BRIGHT_MAGENTA`, `BRIGHT_CYAN`, `BRIGHT_WHITE`

**Background Colors:**
- `BG_BLACK`, `BG_RED`, `BG_GREEN`, `BG_YELLOW`, `BG_BLUE`, `BG_MAGENTA`, `BG_CYAN`, `BG_WHITE`
- `BG_BRIGHT_BLACK`, `BG_BRIGHT_RED`, `BG_BRIGHT_GREEN`, `BG_BRIGHT_YELLOW`, `BG_BRIGHT_BLUE`, `BG_BRIGHT_MAGENTA`, `BG_BRIGHT_CYAN`, `BG_BRIGHT_WHITE`

**Text Attributes:**
- `BOLD`, `DIM`, `ITALIC`, `UNDERLINE`, `SLOW_BLINK`, `RAPID_BLINK`, `INVERTED`, `CONCEAL`, `STRIKETHROUGH`

#### Static Methods

**`apply_style(text: str, *styles: str) -> str`**

Apply one or more styles to text.

```python
styled_text = InputStyle.apply_style("Hello", InputStyle.BOLD, InputStyle.RED)
```

**`color_256(n: int) -> str`**

Generate 256-color foreground color code (0-255).

```python
orange = InputStyle.color_256(208)
```

**`bg_color_256(n: int) -> str`**

Generate 256-color background color code (0-255).

```python
bg_orange = InputStyle.bg_color_256(208)
```

**`rgb_color(r: int, g: int, b: int) -> str`**

Generate RGB true color foreground code.

```python
custom_color = InputStyle.rgb_color(255, 128, 64)
```

**`rgb_bg_color(r: int, g: int, b: int) -> str`**

Generate RGB true color background code.

```python
custom_bg = InputStyle.rgb_bg_color(255, 128, 64)
```

### `InputValidator`

Static validation methods for input constraints.

#### Static Methods

**`validate_length(value: str, min_length: Optional[int], max_length: Optional[int]) -> bool`**

Validate string length constraints.

**`validate_type(value: str, target_type: Type) -> bool`**

Validate if string can be cast to target type.

**`validate_pattern(value: str, pattern: str) -> bool`**

Validate string against regex pattern.

**`validate_ip_address(value: str) -> bool`**

Validate IPv4 address format.

**`validate_in_choices(value: str, choices: List[str]) -> bool`**

Validate string is in allowed choices.

### `InputConfig`

Configuration container for input parameters.

**Constructor Parameters:**
All parameters from `get_input()` function are encapsulated in this class.

**Properties:**
- `styled_prompt`: Generated styled prompt string
- Validation methods for configuration consistency

### `InputHandler`

Handles terminal interaction and character processing.

**Key Methods:**
- `get_input()`: Main input processing loop
- Terminal state management
- Character-by-character input processing
- Cursor movement and buffer management

## Type Casting

The `cast_value(value: str, target_type: Type) -> Any` function handles type conversion:

**Supported Types:**
- `str`: No conversion (passthrough)
- `int`: Integer conversion with error handling
- `float`: Float conversion with error handling
- `bool`: Boolean conversion supporting multiple formats
- Custom types: Calls type constructor

**Boolean Values:**
- **True**: "true", "yes", "t", "y", "1" (case-insensitive)
- **False**: "false", "no", "f", "n", "0" (case-insensitive)

## Error Handling

**Common Exceptions:**
- `ValueError`: Invalid input that fails validation
- `KeyboardInterrupt`: User pressed Ctrl+C
- `EOFError`: End of input (handled gracefully with defaults)

**Validation Flow:**
1. Length validation (if specified)
2. Type validation 
3. Pattern validation (if specified)
4. Choice validation (if specified)
5. Custom validation (if specified)

All validators must pass for input to be accepted.

## Terminal Features

**Supported Key Bindings:**
- **Arrow Keys**: Left/Right for cursor movement
- **Home/End**: Move to start/end of input
- **Backspace**: Delete previous character
- **Enter**: Submit input
- **Ctrl+C**: Cancel input (raises KeyboardInterrupt)

**Terminal Modes:**
- **Terminal Mode**: Full character-by-character input with ANSI support
- **Non-Terminal Mode**: Automatic fallback to standard `input()` for scripts/pipes

**Cross-Platform Support:**
- Primary: Linux/Unix with termios support
- Fallback: Any platform via standard input functions
# Developer Guide

## Getting Started

This guide helps developers understand, extend, and contribute to the robust_input library.

## Development Setup

### Prerequisites

- Python 3.8+ (recommended: 3.12+)
- Linux/Unix environment for full terminal features
- Git for version control

### Installation for Development

1. **Clone the repository:**
```bash
git clone <repository-url>
cd robust_input
```

2. **Set up development environment:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\\Scripts\\activate  # Windows

# Install development dependencies
pip install coverage black isort flake8
```

3. **Verify installation:**
```bash
make validate
make test
```

## Project Structure

```
robust_input/
├── robust_input.py         # Main module implementation
├── test_robust_input.py    # Comprehensive test suite
├── docs/                   # Documentation
│   ├── api-reference.md    # API documentation
│   ├── developer-guide.md  # This file
│   └── architecture.md     # Architecture documentation
├── .github/workflows/      # CI/CD configuration
├── Makefile               # Development commands
├── README.md              # Project overview
├── pyproject.toml         # Package configuration
└── LICENSE                # MIT license
```

## Architecture Overview

### Core Design Principles

1. **Separation of Concerns**: Each class has a single, well-defined responsibility
2. **Configuration Object Pattern**: All parameters encapsulated in `InputConfig`
3. **Strategy Pattern**: Multiple validation strategies through `InputValidator`
4. **Graceful Degradation**: Automatic fallback for non-terminal environments
5. **Resource Management**: Proper terminal state cleanup

### Class Hierarchy

```
InputStyle          # ANSI styling and color utilities
InputValidator      # Static validation methods
InputConfig         # Configuration container with validation
InputHandler        # Terminal interaction and input processing
```

### Data Flow

```
User Input → InputHandler → Validation Chain → Type Casting → Return Value
                ↓
        Terminal Control ← InputConfig ← InputStyle
```

## Key Components

### 1. InputHandler Class

**Purpose**: Manages terminal interaction and character processing

**Key Responsibilities:**
- Raw terminal mode management
- Character-by-character input processing
- Cursor movement and buffer management
- Error display and screen management
- Validation orchestration

**Critical Methods:**
- `get_input()`: Main input loop
- `_read_char()`: Safe character reading with timeouts
- `_process_arrow_keys()`: Handle navigation keys
- `_validate_input()`: Run validation chain

### 2. InputValidator Class

**Purpose**: Provides static validation methods

**Validation Types:**
- Length constraints (min/max)
- Type casting validation
- Regex pattern matching
- Choice selection
- IP address format
- Custom validator functions

**Performance Features:**
- Regex pattern caching
- Pre-compiled validation chains
- Optimized boolean validation

### 3. InputConfig Class

**Purpose**: Configuration container with parameter validation

**Validation Features:**
- Parameter consistency checking
- Regex pattern compilation testing
- Type validation
- Style list validation

### 4. InputStyle Class

**Purpose**: ANSI styling and color management

**Features:**
- Comprehensive ANSI color constants
- 256-color support
- RGB true color support
- Style application utilities

## Performance Optimizations

### 1. Regex Pattern Caching

```python
# Patterns are compiled once and cached
_pattern_cache = {}

@staticmethod
def validate_pattern(value: str, pattern: str) -> bool:
    if pattern not in InputValidator._pattern_cache:
        InputValidator._pattern_cache[pattern] = re.compile(pattern)
    compiled_pattern = InputValidator._pattern_cache[pattern]
    return bool(compiled_pattern.match(value))
```

### 2. Pre-compiled Validation Chains

```python
def _build_validator_chain(self):
    """Build optimized validation chain without lambda overhead."""
    validators = []
    
    if self.config.min_length is not None or self.config.max_length is not None:
        validators.append(('length', self.config.min_length, self.config.max_length))
    
    validators.append(('type', self.config.target_type))
    # ... more validators
    
    return validators
```

### 3. Optimized Buffer Operations

- O(1) character insertion using list-based buffer
- Efficient redraw algorithms for middle insertions
- Minimal ANSI escape sequence usage
- Selective styling to reduce overhead

## Terminal Control

### Key Concepts

**Raw Mode**: Disables line buffering and echo for character-by-character input
**ANSI Escape Sequences**: Used for cursor movement and styling
**Terminal State Management**: Proper cleanup to prevent terminal corruption

### Character Processing

```python
def _read_char(self) -> str:
    """Read a single character with timeout protection."""
    try:
        tty.setraw(sys.stdin.fileno())
        ready, _, _ = select.select([sys.stdin], [], [], 0.1)
        if ready:
            char = sys.stdin.read(1)
        else:
            char = ''
    finally:
        if self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
    
    return char
```

### Escape Sequence Handling

The library handles various terminal escape sequences:

- `\\033[D` / `\\033[C`: Left/Right arrow keys
- `\\033[H` / `\\033[F`: Home/End keys  
- `\\033[1~` / `\\033[4~`: Alternative Home/End sequences

## Testing Strategy

### Test Categories

1. **Unit Tests**: Individual class and method testing
2. **Integration Tests**: Complete workflow testing
3. **Mock Tests**: Terminal operations with proper isolation
4. **Edge Case Tests**: Boundary conditions and error paths

### Mock Strategy

```python
@patch('robust_input.sys.stdin.isatty', return_value=False)
@patch('builtins.input', return_value='test_value')
def test_simple_input_fallback(self, mock_input, mock_isatty):
    """Test fallback to simple input for non-terminal environments."""
    result = self.handler.get_input()
    self.assertEqual(result, 'test_value')
```

### Coverage Analysis

- **Target**: 80%+ overall coverage
- **Focus**: Business logic validation and configuration
- **Exclusions**: Platform-specific terminal operations

## Extending the Library

### Adding New Validation Types

1. **Add static method to InputValidator:**
```python
@staticmethod
def validate_email(value: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return InputValidator.validate_pattern(value, pattern)
```

2. **Update validation chain building:**
```python
def _build_validator_chain(self):
    # ... existing validators
    if self.config.validate_email:
        validators.append(('email', None))
```

3. **Add to InputConfig:**
```python
def __init__(self, ..., validate_email: bool = False):
    self.validate_email = validate_email
```

### Adding New Key Bindings

1. **Extend escape sequence handling:**
```python
def _handle_extended_keys(self, digit: str):
    if final_char == "~":
        if digit == "2":  # Insert key
            self._handle_insert_key()
        elif digit == "3":  # Delete key
            self._handle_delete_key()
```

2. **Implement key behavior:**
```python
def _handle_delete_key(self):
    """Handle Delete key (forward delete)."""
    if self.cursor_pos < len(self.buffer):
        self.buffer.pop(self.cursor_pos)
        self._redraw_from_cursor()
```

### Adding New Convenience Functions

```python
def get_email(
    prompt: str,
    default: Optional[str] = None,
    allow_empty: bool = False,
    **kwargs
) -> str:
    """Get a validated email address."""
    return get_input(
        prompt=prompt,
        default=default,
        allow_empty=allow_empty,
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$',
        error_message="Please enter a valid email address",
        **kwargs
    )
```

## Code Style Guidelines

### Formatting

- **Line Length**: 88 characters (Black default)
- **Import Sorting**: isort with Black compatibility
- **Quote Style**: Double quotes preferred

### Documentation

- **Docstrings**: Google style for all public methods
- **Type Hints**: Required for all parameters and return values
- **Comments**: Explain complex logic, not obvious code

### Example Method Documentation

```python
def validate_length(
    value: str, 
    min_length: Optional[int] = None, 
    max_length: Optional[int] = None
) -> bool:
    """Validate the length of the input string.

    Args:
        value: The input string to validate.
        min_length: The minimum allowed length (inclusive).
        max_length: The maximum allowed length (inclusive).

    Returns:
        True if the length is valid, False otherwise.
    """
```

## Development Workflow

### 1. Development Commands

```bash
# Run tests
make test
make test-verbose

# Check code quality
make lint
make format

# Generate coverage
make coverage

# Validate module
make validate
```

### 2. Pre-commit Checklist

- [ ] All tests pass (`make test`)
- [ ] Code is properly formatted (`make format`)
- [ ] Linting passes (`make lint`)
- [ ] Coverage is acceptable (`make coverage`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)

### 3. Commit Message Format

```
type(scope): brief description

Detailed description of the change, including:
- What was changed and why
- Any breaking changes
- Related issue numbers
```

**Types**: feat, fix, docs, style, refactor, test, chore

## Debugging Tips

### Terminal Issues

1. **Terminal State Corruption:**
```bash
# Reset terminal if corrupted during development
reset
# or
stty sane
```

2. **Debugging Character Input:**
```python
# Add debug prints to see raw character values
char = sys.stdin.read(1)
print(f"Debug: char={repr(char)}, ord={ord(char)}")
```

3. **Testing in Different Environments:**
```bash
# Test non-terminal mode
python script.py < input.txt

# Test with different TERM values
TERM=xterm python script.py
TERM=dumb python script.py
```

### Common Issues

1. **Import Errors**: Ensure module is in Python path
2. **Terminal Features Missing**: Check if running in actual terminal
3. **Test Failures**: Verify mock setup for terminal operations

## Contributing Guidelines

### Pull Request Process

1. **Fork and Branch**: Create feature branch from main
2. **Develop**: Follow coding standards and add tests
3. **Test**: Ensure all tests pass and coverage is maintained
4. **Document**: Update relevant documentation
5. **Review**: Submit PR with clear description

### Code Review Criteria

- [ ] Functionality works as intended
- [ ] Tests cover new functionality
- [ ] Code follows style guidelines
- [ ] Documentation is clear and complete
- [ ] Performance impact is acceptable
- [ ] Backward compatibility is maintained

## Release Process

1. **Version Update**: Update version in `pyproject.toml`
2. **Changelog**: Update `CHANGELOG.md` with changes
3. **Testing**: Run full test suite across Python versions
4. **Documentation**: Ensure docs are up to date
5. **Tag**: Create git tag with version number
6. **Release**: Create GitHub release with notes
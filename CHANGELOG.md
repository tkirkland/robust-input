# Changelog

All notable changes to the robust_input library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-13

### Added
- **Production Stability**: First stable release with comprehensive improvements
- **Cache Size Management**: Added bounded regex pattern cache with FIFO eviction (100 patterns max)
- **Timeout Constants**: Centralized SELECT_TIMEOUT constant for maintainable timing configuration
- **Infinite Loop Protection**: Added max_attempts parameter to prevent endless validation loops
- Comprehensive documentation suite (API reference, developer guide, architecture)
- Complete test suite with 69% coverage (53 tests)
- GitHub Actions CI/CD pipeline
- Makefile for development workflow
- Example applications in `examples/` directory

### Changed
- **Memory Safety**: Pattern cache now has bounded size to prevent memory exhaustion attacks
- **Code Quality**: Eliminated magic numbers by extracting timeout constants
- **Robustness**: Non-terminal environments now have 10-attempt validation limit by default
- **Development Status**: Promoted to Production/Stable classification
- README updated with enhanced examples and better organization

### Fixed
- **Memory DoS Prevention**: Regex pattern cache can no longer grow unbounded
- **Infinite Validation Loops**: Added escape hatch for pathological validation scenarios
- **Code Maintainability**: Centralized timeout values for easier configuration

### Security
- **DoS Resistance**: Enhanced protection against both memory and CPU exhaustion attacks
- **Bounded Behavior**: All operations now have predictable resource usage limits

## [0.9.0] - 2024-12-XX

### Added
- **Home/End Key Support**: Navigate to start/end of input buffer
  - `Home` key or `Ctrl+A`: Move cursor to beginning
  - `End` key or `Ctrl+E`: Move cursor to end
  - Support for both `\033[H`/`\033[F` and `\033[1~`/`\033[4~` sequences

### Fixed
- **Critical Terminal State Bug**: Fixed unreachable finally block in `_read_char()` method
  - Terminal state restoration now guaranteed in all code paths
  - Prevents terminal corruption on unexpected exits
- **Boolean Validation Consistency**: Aligned validation and casting for boolean values
  - Both validation and casting now accept: "true", "yes", "t", "y", "1" (true)
  - Both validation and casting now accept: "false", "no", "f", "n", "0" (false)
- **IP Address Validation**: Fixed leading zero acceptance vulnerability
  - Now correctly rejects "192.168.001.001" (prevents octal interpretation)
  - Maintains acceptance of "0.0.0.0" as valid
- **Terminal Race Conditions**: Added timeout protection to prevent indefinite blocking
  - `_read_char()` now uses 0.1s timeout with `select()`
  - `_process_arrow_keys()` uses timeouts for escape sequence reading

### Improved
- **Performance Optimizations**:
  - Pre-compiled validation chains (eliminates lambda overhead)
  - Regex pattern caching for repeated validations
  - Optimized buffer redraw algorithms (3x faster for large inputs)
  - Efficient string building in styling operations
- **Configuration Parameter Validation**: Added comprehensive validation at initialization
  - Validates length constraints, regex patterns, choices, and type consistency
  - Prevents invalid configurations with clear error messages
- **Error Handling**: Enhanced robustness across all components
  - Better exception handling for malformed escape sequences
  - Graceful degradation for terminal access issues
  - Improved error messages with context

## [0.8.0] - 2024-11-XX

### Added
- **Advanced Terminal Control**:
  - Character-by-character input processing
  - Full cursor movement with arrow keys (left/right)
  - Real-time input validation and feedback
  - Smart error display without screen scrolling
- **Comprehensive Validation System**:
  - Length constraints (min/max)
  - Type validation and casting (str, int, float, bool, custom)
  - Regular expression pattern matching
  - Choice validation from predefined lists
  - Custom validator function support
  - IP address format validation
- **Professional Styling**:
  - Complete ANSI color and style support
  - 256-color and RGB true color support
  - Customizable prompt, input, and error styling
  - Style application utilities
- **Convenience Functions**:
  - `get_password()`: Secure password input with masking
  - `get_integer()`: Integer input with range validation
  - `get_choice()`: Selection from predefined options
  - `get_ip_address()`: IPv4 address validation

### Technical Features
- **Cross-Platform Compatibility**:
  - Full terminal features on Linux/Unix
  - Automatic fallback to `input()` for non-terminal environments
  - Compatible with scripts, pipes, and IDEs
- **Resource Management**:
  - Proper terminal state backup and restoration
  - Exception-safe terminal handling
  - Memory-efficient implementation
- **Architecture**:
  - Clean separation of concerns (4 focused classes)
  - Configuration object pattern
  - Strategy pattern for validation
  - Template method for input processing

## [0.1.0] - 2024-10-XX

### Added
- Initial release of robust_input module
- Basic input functionality with validation
- Simple terminal control
- Core validation methods
- Basic styling support

---

## Migration Guide

### Upgrading to 0.9.0

**No Breaking Changes**: Version 0.9.0 is fully backward compatible with 0.8.0.

**New Features Available**:
- Home/End key navigation works automatically
- Improved error handling provides more stability
- Performance optimizations provide faster validation

**Recommended Actions**:
- Update any custom validators to handle edge cases better
- Consider using the new validation error messages for better UX
- Test with the improved boolean validation if you use boolean inputs

### Upgrading from 0.1.x to 0.8.0+

**Breaking Changes**:
- Module structure reorganized into classes
- Some function signatures changed for consistency
- Error handling behavior improved (may affect exception catching)

**Migration Steps**:

1. **Update Import Structure**:
```python
# Old (0.1.x)
from robust_input import get_input, InputStyle

# New (0.8.0+) - Still works
import robust_input as ri
```

2. **Update Function Calls**:
```python
# Old (0.1.x)
result = get_input("Prompt", validation_func=my_validator)

# New (0.8.0+)
result = ri.get_input("Prompt", custom_validator=my_validator)
```

3. **Update Error Handling**:
```python
# Old (0.1.x)
try:
    result = get_input("Prompt")
except InputError:
    # Handle error

# New (0.8.0+)
try:
    result = ri.get_input("Prompt")
except ValueError:
    # Handle validation error
except KeyboardInterrupt:
    # Handle Ctrl+C
```

4. **Update Styling**:
```python
# Old (0.1.x)
result = get_input("Prompt", color="red")

# New (0.8.0+)
result = ri.get_input(
    "Prompt", 
    prompt_style=[ri.InputStyle.RED, ri.InputStyle.BOLD]
)
```

## Security Updates

### Version 0.9.0
- **Fixed IP validation bypass**: Prevents octal interpretation attacks
- **Enhanced input sanitization**: Better handling of malformed input
- **Terminal state protection**: Guaranteed cleanup prevents terminal corruption

### Version 0.8.0
- **Secure password handling**: No plaintext storage, immediate masking
- **Input bounds checking**: Prevents buffer overflow attempts
- **Safe terminal operations**: Exception handling for all terminal access

## Performance Improvements

### Version 0.9.0
- **3x faster buffer operations** through optimized redraw algorithms
- **O(1) pattern lookup** after first compilation via caching
- **Reduced validation overhead** through pre-compiled chains
- **Minimized ANSI sequences** for better terminal performance

### Version 0.8.0
- **Character-by-character processing** for real-time feedback
- **Efficient cursor management** with minimal screen updates
- **Memory-optimized validation** with minimal object creation

## Known Issues

### Current Limitations
- **Unicode Support**: Limited to ASCII printable characters (32-126)
- **Terminal Width**: No automatic detection for very long inputs
- **Windows Terminal**: Some escape sequences may not work on older Windows terminals
- **Complex Navigation**: Page Up/Down, Insert, Delete keys not yet supported

### Planned Improvements
- Full Unicode character support
- Terminal width detection and line wrapping
- Extended key sequence support
- Windows Terminal compatibility improvements

---

For detailed technical information, see:
- [API Reference](docs/api-reference.md)
- [Developer Guide](docs/developer-guide.md)
- [Architecture Documentation](docs/architecture.md)
- [Testing Documentation](docs/testing.md)
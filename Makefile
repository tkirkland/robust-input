# Makefile for robust_input project

.PHONY: test test-verbose coverage lint format clean help install

# Default target
help:
	@echo "Available targets:"
	@echo "  test         - Run all tests"
	@echo "  test-verbose - Run tests with verbose output"
	@echo "  coverage     - Run tests with coverage report"
	@echo "  lint         - Run code linting"
	@echo "  format       - Format code with black and isort"
	@echo "  clean        - Clean up generated files"
	@echo "  install      - Install package in development mode"
	@echo "  help         - Show this help message"

# Run tests
test:
	python -m unittest test_robust_input

# Run tests with verbose output
test-verbose:
	python -m unittest test_robust_input -v

# Run tests with coverage
coverage:
	python -m coverage run test_robust_input.py
	python -m coverage report robust_input.py
	python -m coverage html robust_input.py
	@echo "Coverage report generated in htmlcov/"

# Lint code
lint:
	@echo "Checking code formatting..."
	python -m black --check robust_input.py test_robust_input.py || (echo "❌ Run 'make format' to fix formatting"; exit 1)
	@echo "Checking import sorting..."
	python -m isort --check-only robust_input.py test_robust_input.py || (echo "❌ Run 'make format' to fix imports"; exit 1)
	@echo "Running flake8..."
	python -m flake8 robust_input.py test_robust_input.py --max-line-length=88 --extend-ignore=E203,W503
	@echo "✅ All linting checks passed"

# Format code
format:
	python -m black robust_input.py test_robust_input.py
	python -m isort robust_input.py test_robust_input.py

# Clean up generated files
clean:
	rm -rf __pycache__/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf *.egg-info/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# Install package in development mode
install:
	pip install -e .

# Validate module imports correctly
validate:
	python -c "import robust_input; print('✅ Module imports successfully')"
	python -m py_compile robust_input.py
	@echo "✅ Module validation passed"
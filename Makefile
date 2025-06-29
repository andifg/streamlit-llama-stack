.PHONY: format sort-imports type-check quality-check help

# Format code with black
format:
	poetry run black .

# Sort imports with isort
sort-imports:
	poetry run isort .

# Type check with mypy
type-check:
	poetry run mypy .

# Run all quality checks
quality-check:
	poetry run black --check .
	poetry run isort --check-only .
	poetry run mypy .

# Fix all quality issues
quality-fix:
	poetry run black .
	poetry run isort .

# Help target
help:
	@echo "Available targets:"
	@echo "  format       - Format code with black"
	@echo "  sort-imports - Sort imports with isort"
	@echo "  type-check   - Type check with mypy"
	@echo "  quality-check - Run all quality checks"
	@echo "  quality-fix  - Fix all quality issues"
	@echo "  help         - Show this help message" 
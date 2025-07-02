.PHONY: format sort-imports type-check quality-check help

# Format code with black
format:
	uv run black .

# Sort imports with isort
sort-imports:
	uv run isort .

# Type check with mypy
type-check:
	uv run mypy .

# Run all quality checks
quality-check:
	uv run black --check .
	uv run isort --check-only .
	uv run mypy .

# Fix all quality issues
quality-fix:
	uv run black .
	uv run isort .

# Help target
help:
	@echo "Available targets:"
	@echo "  format       - Format code with black"
	@echo "  sort-imports - Sort imports with isort"
	@echo "  type-check   - Type check with mypy"
	@echo "  quality-check - Run all quality checks"
	@echo "  quality-fix  - Fix all quality issues"
	@echo "  help         - Show this help message" 
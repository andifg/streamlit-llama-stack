#!/bin/bash

# Quality check script for the project
set -e  # Exit on any error

echo "🔍 Running code quality checks..."

echo "📐 Checking code formatting with black..."
poetry run black --check .

echo "📦 Checking import sorting with isort..."
poetry run isort --check-only .

echo "🔍 Running type checks with mypy..."
poetry run mypy .

echo "✅ All quality checks passed!" 
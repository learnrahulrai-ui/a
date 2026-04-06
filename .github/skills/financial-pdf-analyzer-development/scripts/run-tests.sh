#!/bin/bash
# Run complete test suite with coverage

set -e

echo "📋 Financial PDF Analyzer — Test Suite"
echo "========================================"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Install with: pip install -r requirements.txt"
    exit 1
fi

echo "🧪 Running tests with coverage..."
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing

echo ""
echo "✅ All tests passed!"
echo ""
echo "📊 Coverage Report Summary:"
pytest tests/ --cov=app --cov-report=term-missing --quiet

echo ""
echo "💡 Tip: Run 'pytest tests/ -k <pattern>' to run specific tests"

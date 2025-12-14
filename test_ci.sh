#!/bin/bash
# Local CI Testing Script
# This script tests all CI checks locally before pushing to GitHub

set -e

echo "🧪 Testing CI Checks Locally"
echo "============================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated. Activating...${NC}"
    source venv/bin/activate
fi

echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo "📦 Installing CI dependencies..."
pip install -q safety bandit flake8 black isort pytest pytest-django pytest-cov
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Test 1: Security Check - Safety
echo "🔒 Running Safety Check (vulnerable dependencies)..."
if safety check --short-report; then
    echo -e "${GREEN}✓ Safety check passed${NC}"
else
    echo -e "${YELLOW}⚠️  Safety check found some issues (non-blocking)${NC}"
fi
echo ""

# Test 2: Security Check - Bandit
echo "🛡️  Running Bandit Security Scan..."
if bandit -r . -f txt -q; then
    echo -e "${GREEN}✓ Bandit scan passed${NC}"
else
    echo -e "${YELLOW}⚠️  Bandit found some issues (non-blocking)${NC}"
fi
echo ""

# Test 3: Migration Check
echo "🗄️  Checking for unapplied migrations..."
if python manage.py makemigrations --check --dry-run; then
    echo -e "${GREEN}✓ No unapplied migrations${NC}"
else
    echo -e "${RED}✗ Unapplied migrations found!${NC}"
    exit 1
fi
echo ""

# Test 4: Static Files Collection
echo "📁 Testing static files collection..."
if python manage.py collectstatic --noinput --dry-run > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Static files collection test passed${NC}"
else
    echo -e "${RED}✗ Static files collection failed!${NC}"
    exit 1
fi
echo ""

# Test 5: Linting - Flake8
echo "🔍 Running Flake8 linting..."
if flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; then
    echo -e "${GREEN}✓ Flake8 critical checks passed${NC}"
else
    echo -e "${YELLOW}⚠️  Flake8 found some issues${NC}"
fi
echo ""

# Test 6: Code Formatting - Black
echo "🎨 Checking code formatting with Black..."
if black --check . 2>/dev/null; then
    echo -e "${GREEN}✓ Code formatting is correct${NC}"
else
    echo -e "${YELLOW}⚠️  Code formatting issues found (run: black .)${NC}"
fi
echo ""

# Test 7: Import Sorting - isort
echo "📋 Checking import sorting with isort..."
if isort --check-only . 2>/dev/null; then
    echo -e "${GREEN}✓ Import sorting is correct${NC}"
else
    echo -e "${YELLOW}⚠️  Import sorting issues found (run: isort .)${NC}"
fi
echo ""

# Test 8: Run Tests (if database is available)
echo "🧪 Running pytest tests..."
if python manage.py migrate --check 2>/dev/null; then
    if pytest --tb=short -q; then
        echo -e "${GREEN}✓ All tests passed${NC}"
    else
        echo -e "${RED}✗ Some tests failed!${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  Database not available, skipping tests${NC}"
fi
echo ""

echo "============================"
echo -e "${GREEN}✅ All CI checks completed!${NC}"
echo ""
echo "Next steps:"
echo "1. Review any warnings above"
echo "2. Commit your changes: git add . && git commit -m 'Your message'"
echo "3. Push to GitHub: git push origin main"
echo "4. Check GitHub Actions tab for CI results"


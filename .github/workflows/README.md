# CI/CD Workflows

This directory contains GitHub Actions workflows for continuous integration and deployment.

## Workflows

### django.yml

Main CI workflow that runs on every push and pull request to `main` and `develop` branches.

#### Jobs:

1. **test** - Runs pytest with coverage
   - Sets up PostgreSQL service
   - Runs database migrations
   - Executes all tests
   - Generates coverage reports

2. **lint** - Code quality checks
   - Runs flake8 for code style
   - Checks code formatting with black
   - Verifies import sorting with isort

3. **security** - Security scanning
   - Runs safety check for vulnerable dependencies
   - Scans code with bandit for security issues
   - Generates security reports

4. **migrations** - Database migration checks
   - Verifies no unapplied migrations exist
   - Ensures migration files are up to date

5. **staticfiles** - Static files validation
   - Tests static file collection
   - Verifies static files configuration

## Running Locally

You can test these checks locally:

```bash
# Security checks
pip install safety bandit
safety check
bandit -r . -f txt

# Migration check
python manage.py makemigrations --check --dry-run

# Static files check
python manage.py collectstatic --noinput --dry-run

# Linting
pip install flake8 black isort
flake8 .
black --check .
isort --check-only .
```


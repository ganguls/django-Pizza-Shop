# CI Testing Guide

This guide shows you how to test if your CI/CD pipeline is working correctly.

## 🧪 Method 1: Test Locally (Before Pushing)

### Quick Test Script

Run the automated test script:

```bash
./test_ci.sh
```

This will test all CI checks locally:
- ✅ Security scanning (safety + bandit)
- ✅ Migration checks
- ✅ Static files collection
- ✅ Linting (flake8, black, isort)
- ✅ Unit tests (if database available)

### Manual Testing

Test each CI check individually:

#### 1. Security Checks
```bash
source venv/bin/activate
pip install safety bandit

# Check for vulnerable dependencies
safety scan

# Scan code for security issues
bandit -r . -f txt
```

#### 2. Migration Check
```bash
python manage.py makemigrations --check --dry-run
```

Expected output: `No changes detected`

#### 3. Static Files Collection
```bash
python manage.py collectstatic --noinput --dry-run
```

Expected output: Shows static files that would be collected

#### 4. Linting
```bash
pip install flake8 black isort

# Run flake8
flake8 . --max-line-length=127

# Check formatting
black --check .

# Check import sorting
isort --check-only .
```

#### 5. Run Tests
```bash
pytest --cov=. --cov-report=term
```

---

## 🚀 Method 2: Test on GitHub Actions

### Step 1: Commit Your Changes

```bash
# Add CI workflow files
git add .github/workflows/
git add requirements.txt
git add test_ci.sh
git add CI_TESTING.md

# Commit
git commit -m "Add GitHub Actions CI workflow"

# Push to trigger CI
git push origin main
```

### Step 2: Check GitHub Actions Status

1. **Go to your GitHub repository**
   - Navigate to: `https://github.com/ganguls/django-Pizza-Shop`

2. **Click on "Actions" tab**
   - You'll see a list of workflow runs

3. **Click on the latest workflow run**
   - You'll see all 5 jobs running in parallel:
     - ✅ `test` - Running tests
     - ✅ `lint` - Code quality checks
     - ✅ `security` - Security scanning
     - ✅ `migrations` - Migration validation
     - ✅ `staticfiles` - Static files check

4. **Click on each job to see details**
   - Green checkmark ✅ = Passed
   - Red X ❌ = Failed
   - Yellow circle ⏳ = In progress

### Step 3: View Job Logs

Click on any job to see:
- Installation steps
- Command outputs
- Test results
- Error messages (if any)

### Step 4: Check Artifacts

Some jobs create artifacts:
- **Security job**: Uploads `bandit-report.json`
- **Test job**: Uploads coverage reports

To download:
1. Go to the workflow run
2. Scroll to "Artifacts" section
3. Download the files

---

## 🔍 Troubleshooting

### CI Fails Locally But Works on GitHub

**Issue**: Different Python versions or environments

**Solution**: 
- Use the same Python version (3.11) locally
- Ensure all dependencies are installed

### Migration Check Fails

**Issue**: Unapplied migrations exist

**Solution**:
```bash
python manage.py makemigrations
python manage.py migrate
git add */migrations/
git commit -m "Add migrations"
```

### Static Files Check Fails

**Issue**: Missing static files configuration

**Solution**: Check `settings.py` for:
- `STATIC_URL`
- `STATIC_ROOT`
- `STATICFILES_DIRS`

### Security Check Fails

**Issue**: Vulnerable dependencies found

**Solution**:
```bash
safety scan
# Update vulnerable packages
pip install --upgrade <package-name>
```

### Tests Fail on CI But Pass Locally

**Issue**: Database or environment differences

**Solution**:
- Check PostgreSQL service is running in CI
- Verify environment variables are set correctly
- Check test database configuration

---

## 📊 Understanding CI Results

### Job Status Icons

- ✅ **Green checkmark**: Job passed successfully
- ❌ **Red X**: Job failed (check logs)
- ⏳ **Yellow circle**: Job is running
- ⚠️ **Yellow triangle**: Job passed with warnings

### Common Issues

1. **"No such file or directory"**
   - Missing files in repository
   - Check `.gitignore` isn't excluding needed files

2. **"Module not found"**
   - Missing dependencies in `requirements.txt`
   - Add missing packages

3. **"Database connection failed"**
   - PostgreSQL service not started
   - Check service configuration in workflow

4. **"Permission denied"**
   - File permissions issue
   - Check file permissions in repository

---

## 🎯 Quick Verification Checklist

Before pushing, verify locally:

- [ ] `./test_ci.sh` runs without errors
- [ ] `python manage.py makemigrations --check --dry-run` passes
- [ ] `python manage.py collectstatic --noinput --dry-run` works
- [ ] `pytest` runs successfully
- [ ] `safety scan` shows no critical vulnerabilities
- [ ] `bandit -r .` shows acceptable security level

After pushing:

- [ ] GitHub Actions tab shows workflow running
- [ ] All 5 jobs complete successfully
- [ ] No red X marks
- [ ] Coverage reports are generated
- [ ] Security reports are available

---

## 🔗 Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [View Your Workflow Runs](https://github.com/ganguls/django-Pizza-Shop/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Safety Documentation](https://pyup.io/safety/)
- [Bandit Documentation](https://bandit.readthedocs.io/)

---

## 💡 Tips

1. **Test locally first** - Saves time and CI minutes
2. **Check logs carefully** - CI logs show exactly what failed
3. **Fix one issue at a time** - Easier to debug
4. **Use `continue-on-error: true`** - For non-critical checks
5. **Monitor regularly** - Check CI status after each push

---

**Happy Testing! 🎉**


# Security Guidelines

## 🔒 **Sensitive Information Handling**

This repository handles sensitive device credentials and network information. Follow these security guidelines:

### **Environment Variables**
- **NEVER** commit actual credentials to version control
- Use `.env` files for local development (already in `.gitignore`)
- Set environment variables in CI/CD systems securely

### **Required Environment Variables**
```bash
WATTBOX_TEST_HOST=192.168.1.100        # Your Wattbox device IP
WATTBOX_TEST_USERNAME=wattbox          # Device username
WATTBOX_TEST_PASSWORD=your_password    # Device password
WATTBOX_TEST_PORT=23                   # Telnet port (default: 23)
WATTBOX_TEST_TIMEOUT=10                # Connection timeout
WATTBOX_TEST_SCAN_INTERVAL=20          # Polling interval
```

### **Setup Instructions**

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your actual credentials:**
   ```bash
   nano .env
   ```

3. **Verify `.env` is in `.gitignore`:**
   ```bash
   git status  # Should not show .env
   ```

### **Testing with Real Devices**

- Use environment variables for all device connections
- Never hardcode IP addresses, usernames, or passwords
- Use example values in documentation and tests

### **CI/CD Security**

- Store sensitive values as GitHub Secrets
- Use environment variables in GitHub Actions
- Never log sensitive information

## 🚨 **If Credentials Are Exposed**

If you accidentally commit sensitive information:

1. **Immediately change the exposed credentials**
2. **Remove from git history:**
   ```bash
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch .env' \
   --prune-empty --tag-name-filter cat -- --all
   ```
3. **Force push to remove from remote:**
   ```bash
   git push origin --force --all
   ```

## 📋 **Security Checklist**

- [ ] No hardcoded credentials in source code
- [ ] `.env` file in `.gitignore`
- [ ] Environment variables used for all sensitive data
- [ ] Example values used in documentation
- [ ] CI/CD uses secure secrets management
- [ ] Regular credential rotation

## 🔍 **Security Audit**

To check for potential security issues:

```bash
# Search for hardcoded IPs
grep -r "192\.168\." . --exclude-dir=.git

# Search for potential passwords
grep -r "password.*=" . --exclude-dir=.git --exclude="*.md"

# Check for .env files
find . -name ".env*" -not -path "./.git/*"
```

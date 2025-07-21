#!/bin/bash

# Kiro AI IDE - Security Scanner Hook
# Automated security analysis for code changes

set -euo pipefail

TARGET_PATH="${1:-.}"
SCAN_TYPE="${2:-comprehensive}"

echo "🛡️  Running Kiro AI security scan on: $TARGET_PATH"

# Security check functions
check_hardcoded_secrets() {
    echo "🔍 Checking for hardcoded secrets..."
    
    local secrets_found=false
    local patterns=(
        "password\s*=\s*[\"'][^\"']+[\"']"
        "api[_-]?key\s*=\s*[\"'][^\"']+[\"']"
        "secret[_-]?key\s*=\s*[\"'][^\"']+[\"']"
        "token\s*=\s*[\"'][^\"']+[\"']"
        "private[_-]?key\s*=\s*[\"'][^\"']+[\"']"
        "access[_-]?key\s*=\s*[\"'][^\"']+[\"']"
        "database[_-]?url\s*=\s*[\"'][^\"']+[\"']"
    )
    
    for pattern in "${patterns[@]}"; do
        if find "$TARGET_PATH" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" -o -name "*.json" -o -name "*.yml" -o -name "*.yaml" \) -exec grep -iHn -E "$pattern" {} \; 2>/dev/null | head -10; then
            secrets_found=true
        fi
    done
    
    if [ "$secrets_found" = true ]; then
        echo "❌ Potential hardcoded secrets detected!"
        echo "💡 Use environment variables or secure vaults instead"
        return 1
    else
        echo "✅ No hardcoded secrets detected"
        return 0
    fi
}

check_sql_injection() {
    echo "🔍 Checking for SQL injection vulnerabilities..."
    
    local vulnerabilities_found=false
    local patterns=(
        "SELECT.*\+.*WHERE"
        "INSERT.*\+.*VALUES"
        "UPDATE.*\+.*SET"
        "DELETE.*\+.*WHERE"
        "execute\([^)]*\+[^)]*\)"
        "query\([^)]*\+[^)]*\)"
    )
    
    for pattern in "${patterns[@]}"; do
        if find "$TARGET_PATH" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" \) -exec grep -iHn -E "$pattern" {} \; 2>/dev/null | head -5; then
            vulnerabilities_found=true
        fi
    done
    
    if [ "$vulnerabilities_found" = true ]; then
        echo "⚠️  Potential SQL injection vulnerabilities detected!"
        echo "💡 Use parameterised queries or ORM methods"
        return 1
    else
        echo "✅ No SQL injection patterns detected"
        return 0
    fi
}

check_xss_vulnerabilities() {
    echo "🔍 Checking for XSS vulnerabilities..."
    
    local vulnerabilities_found=false
    local patterns=(
        "innerHTML\s*=\s*.*\+.*"
        "document\.write\([^)]*\+[^)]*\)"
        "eval\([^)]*\+[^)]*\)"
        "dangerouslySetInnerHTML"
        "v-html\s*="
    )
    
    for pattern in "${patterns[@]}"; do
        if find "$TARGET_PATH" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.tsx" -o -name "*.vue" \) -exec grep -iHn -E "$pattern" {} \; 2>/dev/null | head -5; then
            vulnerabilities_found=true
        fi
    done
    
    if [ "$vulnerabilities_found" = true ]; then
        echo "⚠️  Potential XSS vulnerabilities detected!"
        echo "💡 Sanitise user input and use safe DOM manipulation methods"
        return 1
    else
        echo "✅ No XSS patterns detected"
        return 0
    fi
}

check_insecure_randomness() {
    echo "🔍 Checking for insecure randomness..."
    
    local vulnerabilities_found=false
    local patterns=(
        "Math\.random\(\)"
        "Random\(\)\.Next"
        "rand\.Intn"
        "random\.randint"
    )
    
    for pattern in "${patterns[@]}"; do
        if find "$TARGET_PATH" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" -o -name "*.cs" \) -exec grep -Hn -E "$pattern" {} \; 2>/dev/null | head -5; then
            vulnerabilities_found=true
        fi
    done
    
    if [ "$vulnerabilities_found" = true ]; then
        echo "⚠️  Insecure randomness detected!"
        echo "💡 Use cryptographically secure random functions for security-sensitive operations"
        return 1
    else
        echo "✅ No insecure randomness patterns detected"
        return 0
    fi
}

check_insecure_communications() {
    echo "🔍 Checking for insecure communications..."
    
    local vulnerabilities_found=false
    local patterns=(
        "http://[^/]*\."
        "ftp://[^/]*\."
        "verify\s*=\s*False"
        "verify:\s*false"
        "ssl_verify\s*=\s*False"
        "TrustAllCerts"
    )
    
    for pattern in "${patterns[@]}"; do
        if find "$TARGET_PATH" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" -o -name "*.json" -o -name "*.yml" \) -exec grep -iHn -E "$pattern" {} \; 2>/dev/null | head -5; then
            vulnerabilities_found=true
        fi
    done
    
    if [ "$vulnerabilities_found" = true ]; then
        echo "⚠️  Insecure communications detected!"
        echo "💡 Use HTTPS and enable SSL certificate verification"
        return 1
    else
        echo "✅ No insecure communication patterns detected"
        return 0
    fi
}

check_dependency_vulnerabilities() {
    echo "🔍 Checking for vulnerable dependencies..."
    
    # Check package.json
    if [[ -f "package.json" ]]; then
        echo "📦 Found package.json - checking for known vulnerabilities..."
        if command -v npm &> /dev/null; then
            if npm audit --audit-level=moderate 2>/dev/null | grep -i "vulnerabilities"; then
                echo "⚠️  npm audit found vulnerabilities!"
                echo "💡 Run 'npm audit fix' to resolve issues"
                return 1
            fi
        fi
    fi
    
    # Check requirements.txt
    if [[ -f "requirements.txt" ]]; then
        echo "🐍 Found requirements.txt - checking for known vulnerabilities..."
        if command -v safety &> /dev/null; then
            if safety check -r requirements.txt 2>/dev/null | grep -i "vulnerability"; then
                echo "⚠️  Python safety check found vulnerabilities!"
                echo "💡 Update vulnerable packages"
                return 1
            fi
        fi
    fi
    
    # Check go.mod
    if [[ -f "go.mod" ]]; then
        echo "🐹 Found go.mod - checking for known vulnerabilities..."
        if command -v govulncheck &> /dev/null; then
            if govulncheck ./... 2>/dev/null | grep -i "vulnerability"; then
                echo "⚠️  Go vulnerability check found issues!"
                echo "💡 Update vulnerable modules"
                return 1
            fi
        fi
    fi
    
    echo "✅ Dependency vulnerability check complete"
    return 0
}

check_file_permissions() {
    echo "🔍 Checking file permissions..."
    
    local issues_found=false
    
    # Check for overly permissive files
    if find "$TARGET_PATH" -type f -perm -o+w 2>/dev/null | head -5 | grep -q .; then
        echo "⚠️  World-writable files detected!"
        find "$TARGET_PATH" -type f -perm -o+w 2>/dev/null | head -5
        issues_found=true
    fi
    
    # Check for executable scripts without proper permissions
    if find "$TARGET_PATH" -name "*.sh" -o -name "*.py" -o -name "*.pl" | xargs ls -la 2>/dev/null | grep -v "^-rwxr--r--" | head -5 | grep -q .; then
        echo "💡 Consider setting appropriate permissions for executable scripts"
    fi
    
    if [ "$issues_found" = true ]; then
        echo "💡 Fix file permissions using chmod"
        return 1
    else
        echo "✅ File permissions look good"
        return 0
    fi
}

generate_security_report() {
    echo ""
    echo "🛡️  Security Scan Report"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Scanned: $TARGET_PATH"
    echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Type: $SCAN_TYPE"
    echo ""
    
    if [ ${#security_issues[@]} -eq 0 ]; then
        echo "🎉 No security issues detected!"
        echo ""
        echo "✅ All security checks passed:"
        echo "   • No hardcoded secrets"
        echo "   • No SQL injection patterns"
        echo "   • No XSS vulnerabilities"
        echo "   • Secure randomness usage"
        echo "   • Secure communications"
        echo "   • No vulnerable dependencies"
        echo "   • Appropriate file permissions"
    else
        echo "⚠️  Security issues detected:"
        for issue in "${security_issues[@]}"; do
            echo "   • $issue"
        done
        echo ""
        echo "🔧 Recommended Actions:"
        echo "   • Review and fix identified issues"
        echo "   • Run security scan again after fixes"
        echo "   • Consider adding security tests"
        echo "   • Implement security monitoring"
    fi
    echo ""
}

# Main security scan process
main() {
    echo "🎯 Security Scan Configuration:"
    echo "  Target: $TARGET_PATH"
    echo "  Scan Type: $SCAN_TYPE"
    echo ""
    
    declare -a security_issues=()
    
    # Run all security checks
    check_hardcoded_secrets || security_issues+=("Hardcoded secrets detected")
    check_sql_injection || security_issues+=("SQL injection vulnerabilities")
    check_xss_vulnerabilities || security_issues+=("XSS vulnerabilities")
    check_insecure_randomness || security_issues+=("Insecure randomness usage")
    check_insecure_communications || security_issues+=("Insecure communications")
    check_dependency_vulnerabilities || security_issues+=("Vulnerable dependencies")
    check_file_permissions || security_issues+=("File permission issues")
    
    generate_security_report
    
    if [ ${#security_issues[@]} -gt 0 ]; then
        echo "❌ Security scan failed - issues found!"
        exit 1
    else
        echo "✅ Security scan passed!"
        exit 0
    fi
}

main "$@"
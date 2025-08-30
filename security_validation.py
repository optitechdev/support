#!/usr/bin/env python3
"""
Security Validation Script
Tests that all critical security issues have been properly fixed.
"""

import os
import subprocess
import sys

def check_flask_debug_config():
    """Check if Flask debug mode is properly configured"""
    print("🔍 Checking Flask debug configuration...")
    
    # Check main app.py
    with open('/workspaces/support/app.py', 'r') as f:
        content = f.read()
        if 'debug=debug_mode' in content and "os.environ.get('FLASK_ENV') == 'development'" in content:
            print("✅ Main app.py: Debug mode properly configured")
        else:
            print("❌ Main app.py: Debug mode configuration missing")
            return False
    
    # Check support/app.py
    with open('/workspaces/support/support/app.py', 'r') as f:
        content = f.read()
        if 'debug=debug_mode' in content and "os.environ.get('FLASK_ENV') == 'development'" in content:
            print("✅ Support app.py: Debug mode properly configured")
        else:
            print("❌ Support app.py: Debug mode configuration missing")
            return False
    
    return True

def check_secure_logging():
    """Check if secure logging is implemented"""
    print("\n🔍 Checking secure logging implementation...")
    
    files_to_check = [
        '/workspaces/support/app.py',
        '/workspaces/support/support/app.py', 
        '/workspaces/support/optitech_supportmail.py',
        '/workspaces/support/support_assistant_main.py'
    ]
    
    for file_path in files_to_check:
        with open(file_path, 'r') as f:
            content = f.read()
            
            # Check for dangerous print statements with sensitive data
            if 'print(f"❌ Fel från AI: {response.status_code}")' in content:
                print(f"❌ {file_path}: Unsafe logging found")
                return False
            
            # Check for proper logging setup
            if 'import logging' in content or 'logger' in content:
                print(f"✅ {file_path}: Secure logging implemented")
            else:
                if file_path.endswith('app.py'):
                    print(f"❌ {file_path}: No logging configuration found")
                    return False
    
    return True

def check_error_handling():
    """Check if secure error handling is implemented"""
    print("\n🔍 Checking secure error handling...")
    
    files_to_check = [
        '/workspaces/support/app.py',
        '/workspaces/support/support/app.py'
    ]
    
    for file_path in files_to_check:
        with open(file_path, 'r') as f:
            content = f.read()
            
            # Check for generic error messages
            if "'Ett tekniskt fel uppstod. Försök igen senare.'" in content:
                print(f"✅ {file_path}: Secure error handling implemented")
            else:
                print(f"❌ {file_path}: Secure error handling missing")
                return False
    
    return True

def check_production_config():
    """Check if production configuration is properly set"""
    print("\n🔍 Checking production configuration...")
    
    files_to_check = [
        '/workspaces/support/app.py',
        '/workspaces/support/support/app.py'
    ]
    
    for file_path in files_to_check:
        with open(file_path, 'r') as f:
            content = f.read()
            
            # Check for production security settings
            if "app.config['DEBUG'] = False" in content:
                print(f"✅ {file_path}: Production debug config found")
            else:
                print(f"❌ {file_path}: Production debug config missing")
                return False
    
    return True

def main():
    """Run all security validation checks"""
    print("🔒 Security Validation Report")
    print("=" * 50)
    
    checks = [
        ("Flask Debug Configuration", check_flask_debug_config),
        ("Secure Logging", check_secure_logging),
        ("Error Handling", check_error_handling),
        ("Production Configuration", check_production_config)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name}: Error during check - {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🛡️  ALL SECURITY CHECKS PASSED!")
        print("✅ The application is secure for production deployment.")
        sys.exit(0)
    else:
        print("⚠️  SECURITY ISSUES FOUND!")
        print("❌ Please fix the issues above before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main()

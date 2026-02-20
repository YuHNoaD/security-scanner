# Sample vulnerable application for testing security scanner

import sqlite3
import os
import subprocess

# VULNERABILITY 1: SQL Injection (CRITICAL)
def get_user_info(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # SQL Injection vulnerability - using f-string with user input
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchall()

# VULNERABILITY 2: SQL Injection with concatenation (CRITICAL)
def search_users(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # SQL Injection - string concatenation
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()

# VULNERABILITY 3: XSS (HIGH)
def render_user_input(user_input):
    # XSS vulnerability - directly embedding user input in HTML
    html = f"<div>Welcome, {user_input}!</div>"
    return html

# VULNERABILITY 4: XSS with innerHTML (HIGH)
def update_dashboard(data):
    # XSS vulnerability - using innerHTML with user data
    return f"document.getElementById('dashboard').innerHTML = '{data}'"

# VULNERABILITY 5: Command Injection (CRITICAL)
def run_command(filename):
    # Command Injection - using os.system with user input
    os.system(f"cat {filename}")

# VULNERABILITY 6: Command Injection with subprocess (CRITICAL)
def process_file(filepath):
    # Command Injection - subprocess with user input
    subprocess.run(['ls', filepath], shell=True)

# VULNERABILITY 7: Hardcoded API Key (CRITICAL)
api_key = "sk-1234567890abcdefghijklmnopqrstuvwxyz"

def make_api_request():
    # Hardcoded API key
    return f"Authorization: Bearer {api_key}"

# VULNERABILITY 8: Hardcoded Password (CRITICAL)
database_password = "admin123"

def connect_to_db():
    # Hardcoded password
    return {"password": database_password}

# VULNERABILITY 9: Hardcoded AWS Secret (CRITICAL)
aws_access_key_id = "AKIAIOSFODNN7EXAMPLE"
aws_secret_access_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def get_aws_credentials():
    # Hardcoded AWS credentials
    return {
        "access_key": aws_access_key_id,
        "secret_key": aws_secret_access_key
    }

# VULNERABILITY 10: Hardcoded Token (CRITICAL)
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"

def authenticate():
    # Hardcoded authentication token
    return {"token": auth_token}

# Safe code example (should not trigger any alerts)
def safe_function():
    # This is safe - no vulnerabilities
    result = 2 + 2
    return result
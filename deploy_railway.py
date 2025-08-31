#!/usr/bin/env python3
"""
Railway Deployment Helper Script
Run this to deploy your AgriMarket API to Railway
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check if Node.js is installed
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        print("✅ Node.js is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js is not installed. Please install it from https://nodejs.org/")
        return False
    
    # Check if Railway CLI is installed
    try:
        subprocess.run(["railway", "--version"], check=True, capture_output=True)
        print("✅ Railway CLI is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Railway CLI is not installed. Installing now...")
        result = run_command("npm install -g @railway/cli", "Installing Railway CLI")
        if not result:
            return False
    
    return True

def deploy_to_railway():
    """Deploy the application to Railway"""
    print("🚀 Starting Railway deployment...")
    
    # Check if already initialized
    if os.path.exists(".railway"):
        print("ℹ️  Railway project already initialized")
    else:
        print("🆕 Initializing new Railway project...")
        result = run_command("railway init", "Initializing Railway project")
        if not result:
            return False
    
    # Deploy the application
    print("📤 Deploying to Railway...")
    result = run_command("railway up", "Deploying to Railway")
    if not result:
        return False
    
    # Get the domain
    print("🌐 Getting deployment URL...")
    domain = run_command("railway domain", "Getting Railway domain")
    if domain:
        print(f"🎉 Deployment successful!")
        print(f"🌍 Your API is live at: {domain}")
        print(f"📊 Test it with: curl {domain}/")
        print(f"🔍 Data endpoint: {domain}/request?commodity=Rice&state=Maharashtra&market=Mumbai")
    else:
        print("⚠️  Deployment completed but couldn't get domain")
    
    return True

def main():
    """Main deployment function"""
    print("🚀 AgriMarket API Railway Deployment")
    print("=" * 40)
    
    if not check_requirements():
        print("❌ Requirements check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Check if user is logged in
    try:
        subprocess.run(["railway", "whoami"], check=True, capture_output=True)
        print("✅ Logged in to Railway")
    except subprocess.CalledProcessError:
        print("🔐 Please login to Railway first:")
        print("   railway login")
        sys.exit(1)
    
    if deploy_to_railway():
        print("\n🎉 Deployment completed successfully!")
        print("📚 Check DEPLOYMENT.md for more deployment options")
    else:
        print("\n❌ Deployment failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

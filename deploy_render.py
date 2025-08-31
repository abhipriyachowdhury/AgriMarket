#!/usr/bin/env python3
"""
Render Deployment Helper Script
This script helps you deploy your AgriMarket API to Render
"""

import webbrowser
import os
import subprocess
import sys

def check_git():
    """Check if git is installed and configured"""
    print("🔍 Checking Git configuration...")
    
    try:
        # Check if git is installed
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git is installed")
        
        # Check if git is configured
        result = subprocess.run(["git", "config", "--global", "user.name"], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("✅ Git user.name is configured")
        else:
            print("⚠️  Git user.name not configured")
            name = input("Enter your Git username: ")
            subprocess.run(["git", "config", "--global", "user.name", name])
        
        result = subprocess.run(["git", "config", "--global", "user.email"], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("✅ Git user.email is configured")
        else:
            print("⚠️  Git user.email not configured")
            email = input("Enter your Git email: ")
            subprocess.run(["git", "config", "--global", "user.email", email])
            
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed. Please install Git from https://git-scm.com/")
        return False

def initialize_git_repo():
    """Initialize git repository if not already done"""
    if not os.path.exists(".git"):
        print("🆕 Initializing Git repository...")
        subprocess.run(["git", "init"])
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Initial commit for Render deployment"])
        print("✅ Git repository initialized")
    else:
        print("ℹ️  Git repository already exists")
        # Add any new files
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Update for Render deployment"])

def open_render_dashboard():
    """Open Render dashboard in browser"""
    print("🌐 Opening Render dashboard...")
    webbrowser.open("https://render.com/dashboard")
    print("✅ Render dashboard opened in your browser")

def show_deployment_steps():
    """Show step-by-step deployment instructions"""
    print("\n" + "="*60)
    print("🚀 RENDER DEPLOYMENT STEPS")
    print("="*60)
    
    print("\n1️⃣  SIGN UP/LOGIN TO RENDER")
    print("   • Go to https://render.com")
    print("   • Sign up with GitHub or create account")
    print("   • Login to dashboard")
    
    print("\n2️⃣  CONNECT YOUR GITHUB REPOSITORY")
    print("   • Click 'New +' button")
    print("   • Select 'Web Service'")
    print("   • Connect your GitHub account")
    print("   • Select this repository")
    
    print("\n3️⃣  CONFIGURE YOUR SERVICE")
    print("   • Name: agrimarket-api (or your preferred name)")
    print("   • Environment: Python")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: gunicorn APIwebScraping:app")
    print("   • Plan: Free")
    
    print("\n4️⃣  DEPLOY")
    print("   • Click 'Create Web Service'")
    print("   • Wait for build to complete")
    print("   • Get your live URL!")
    
    print("\n5️⃣  TEST YOUR API")
    print("   • Your API will be available at: https://your-app-name.onrender.com")
    print("   • Test with: curl https://your-app-name.onrender.com/")
    
    print("\n" + "="*60)

def create_github_repo_instructions():
    """Show instructions for creating GitHub repository"""
    print("\n📚 GITHUB REPOSITORY SETUP")
    print("-" * 40)
    
    print("If you don't have a GitHub repository yet:")
    print("1. Go to https://github.com")
    print("2. Click 'New repository'")
    print("3. Name it: AgriMarket")
    print("4. Make it Public")
    print("5. Don't initialize with README (we already have files)")
    print("6. Click 'Create repository'")
    print("7. Follow the 'push an existing repository' instructions:")
    
    print("\nRun these commands in your terminal:")
    print("git remote add origin https://github.com/YOUR_USERNAME/AgriMarket.git")
    print("git branch -M main")
    print("git push -u origin main")

def main():
    """Main deployment function"""
    print("🚀 AgriMarket API Render Deployment")
    print("=" * 50)
    
    # Check git configuration
    if not check_git():
        print("❌ Git setup failed. Please fix the issues above.")
        sys.exit(1)
    
    # Initialize git repository
    initialize_git_repo()
    
    # Show deployment steps
    show_deployment_steps()
    
    # Ask if user wants to open Render dashboard
    open_dashboard = input("\n❓ Open Render dashboard in browser? (y/n): ").lower()
    if open_dashboard in ['y', 'yes']:
        open_render_dashboard()
    
    # Show GitHub setup if needed
    setup_github = input("\n❓ Do you need help setting up GitHub repository? (y/n): ").lower()
    if setup_github in ['y', 'yes']:
        create_github_repo_instructions()
    
    print("\n🎉 Setup complete! Follow the steps above to deploy to Render.")
    print("📚 Your API will be live at: https://your-app-name.onrender.com")

if __name__ == "__main__":
    main()

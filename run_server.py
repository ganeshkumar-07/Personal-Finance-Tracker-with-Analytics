"""
Personal Finance Tracker - Server Runner
Cross-platform script to start the Flask web server
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'matplotlib', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("⚠️  Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Error installing packages. Please run manually:")
            print("   pip install -r requirements.txt")
            return False
    else:
        print("✅ All required packages are installed!")
    
    return True

def start_server():
    """Start the Flask web server"""
    print("\n" + "="*50)
    print("  Personal Finance Tracker - Web Server")
    print("="*50)
    print("\n🚀 Starting Flask web server...")
    print("\n📍 The application will be available at:")
    print("   http://localhost:5000")
    print("\n⚠️  Press Ctrl+C to stop the server\n")
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if check_dependencies():
        start_server()
    else:
        sys.exit(1)


#!/usr/bin/env python3
"""
Automated Revenue System Launcher
Starts all revenue streams and the web dashboard
"""

import asyncio
import subprocess
import time
import sys
import os
import signal
import threading
from pathlib import Path

def install_dependencies():
    """Install required Python packages"""
    print("🔧 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def start_web_server():
    """Start the FastAPI web server"""
    print("🌐 Starting web dashboard...")
    try:
        # Start the web server
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
    except Exception as e:
        print(f"❌ Error starting web server: {e}")

def start_automation():
    """Start the automation scheduler"""
    print("🤖 Starting automation systems...")
    try:
        from automation_scheduler import run_standalone_automation
        asyncio.run(run_standalone_automation())
    except Exception as e:
        print(f"❌ Error starting automation: {e}")

def main():
    """Main startup function"""
    print("🚀 Starting Automated Revenue System...")
    print("=" * 50)
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found!")
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    print("\n🎯 Revenue streams being activated:")
    print("   💼 Affiliate Marketing")
    print("   📝 Content Monetization") 
    print("   📈 Trading Bot")
    print("   🎯 Ad Optimization")
    print("   💎 Digital Products")
    print("   🤖 AI Services")
    
    print("\n🌟 Features:")
    print("   ✅ Fully automated operation")
    print("   ✅ Real-time revenue tracking")
    print("   ✅ Automatic optimization")
    print("   ✅ Risk management")
    print("   ✅ Multi-stream diversification")
    
    print(f"\n🎊 Dashboard will be available at: http://localhost:8000")
    print("📊 Monitor your passive income in real-time!")
    
    # Start automation in background thread
    automation_thread = threading.Thread(target=start_automation, daemon=True)
    automation_thread.start()
    
    # Small delay to let automation start
    time.sleep(2)
    
    # Start web server (this will block)
    try:
        start_web_server()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down revenue system...")
        print("💰 Revenue generation stopped.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
💰 Automated Revenue System - Desktop Monitor
Alternative way to view your revenue without browser
"""

import requests
import json
import time
import os
import sys
from datetime import datetime

class RevenueMonitor:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.running = True
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def get_revenue_data(self):
        """Fetch current revenue data from the API"""
        try:
            response = requests.get(f"{self.base_url}/api/revenue/summary", timeout=5)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
            
    def get_status_data(self):
        """Fetch system status from the API"""
        try:
            response = requests.get(f"{self.base_url}/api/status", timeout=5)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
            
    def format_currency(self, amount):
        """Format currency with color"""
        return f"${amount:,.2f}"
        
    def print_header(self):
        """Print the dashboard header"""
        print("="*80)
        print("💰 AUTOMATED REVENUE SYSTEM - LIVE DASHBOARD 💰".center(80))
        print("="*80)
        print(f"⏰ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*80)
        
    def print_revenue_summary(self, data):
        """Print revenue summary"""
        if "error" in data:
            print("❌ ERROR: Cannot connect to revenue system")
            print(f"   {data['error']}")
            print("   Make sure the system is running: ./start_money_maker.sh")
            return
            
        print("📊 REVENUE SUMMARY:")
        print(f"   💰 Total Today: {self.format_currency(data['total_revenue_today'])}")
        print(f"   📅 Monthly Projection: {self.format_currency(data['projected_monthly'])}")
        print()
        
        print("💼 REVENUE BREAKDOWN:")
        breakdown = data['breakdown']
        print(f"   🔗 Affiliate Marketing: {self.format_currency(breakdown['affiliate_marketing'])}")
        print(f"   🤖 Automated Trading:   {self.format_currency(breakdown['automated_trading'])}")
        print(f"   📝 Content Revenue:     {self.format_currency(breakdown['content_monetization'])}")
        print(f"   🎯 Ad Optimization:     {self.format_currency(breakdown['ad_optimization'])}")
        print(f"   💎 Product Sales:       {self.format_currency(breakdown['product_sales'])}")
        print()
        
    def print_system_status(self, data):
        """Print system status"""
        if "error" in data:
            print("❌ SYSTEM STATUS: OFFLINE")
            return
            
        print("🚀 SYSTEM STATUS:")
        print(f"   Status: {data['status'].upper()} ✅")
        print(f"   Systems Active: {data['systems_active']}/5")
        print(f"   Uptime: {data['uptime']}")
        print(f"   Message: {data['message']}")
        print()
        
    def print_controls(self):
        """Print control instructions"""
        print("-"*80)
        print("🎛️  CONTROLS:")
        print("   [R] Refresh Now   [Q] Quit   [S] System Status   [O] Optimize")
        print("   [B] Open Browser  [H] Help")
        print("-"*80)
        
    def print_growth_indicator(self, current_revenue):
        """Show revenue growth animation"""
        growth_chars = ["📈", "💹", "🚀", "💰"]
        char = growth_chars[int(time.time()) % len(growth_chars)]
        print(f"{char} MAKING MONEY: {self.format_currency(current_revenue)} and growing!")
        
    def run_interactive(self):
        """Run the interactive dashboard"""
        print("🚀 Starting Revenue Monitor...")
        print("Press Ctrl+C to exit")
        time.sleep(1)
        
        try:
            while self.running:
                self.clear_screen()
                self.print_header()
                
                # Get data
                revenue_data = self.get_revenue_data()
                status_data = self.get_status_data()
                
                # Print dashboard
                self.print_revenue_summary(revenue_data)
                self.print_system_status(status_data)
                
                if "total_revenue_today" in revenue_data:
                    self.print_growth_indicator(revenue_data["total_revenue_today"])
                
                self.print_controls()
                
                # Auto-refresh every 5 seconds or wait for input
                print("\n⏱️  Auto-refreshing in 5 seconds... (press Enter to refresh now)")
                
                # Non-blocking input with timeout
                import select
                import sys
                
                if sys.platform != 'win32':
                    # Unix-like systems
                    ready, _, _ = select.select([sys.stdin], [], [], 5)
                    if ready:
                        user_input = sys.stdin.readline().strip().lower()
                        self.handle_command(user_input)
                else:
                    # Windows - just wait 5 seconds
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            print("\n\n💰 Revenue Monitor stopped. Your system is still making money!")
            print("🌐 Access dashboard at: http://localhost:8000")
            
    def handle_command(self, command):
        """Handle user commands"""
        if command == 'q':
            self.running = False
        elif command == 'r':
            pass  # Just refresh
        elif command == 's':
            self.show_detailed_status()
        elif command == 'o':
            self.optimize_system()
        elif command == 'b':
            self.open_browser()
        elif command == 'h':
            self.show_help()
            
    def show_detailed_status(self):
        """Show detailed system status"""
        print("\n🔍 DETAILED SYSTEM STATUS:")
        try:
            response = requests.get(f"{self.base_url}/api/status")
            data = response.json()
            print(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Error: {e}")
        input("\nPress Enter to continue...")
        
    def optimize_system(self):
        """Optimize the revenue system"""
        print("\n⚡ OPTIMIZING REVENUE SYSTEMS...")
        try:
            response = requests.get(f"{self.base_url}/api/optimize")
            data = response.json()
            print(f"✅ {data['status']}")
            print(f"📈 Performance Improvement: {data['performance_improvement']}")
            print(f"💰 Additional Revenue: {data['estimated_additional_revenue']}")
        except Exception as e:
            print(f"Error: {e}")
        input("\nPress Enter to continue...")
        
    def open_browser(self):
        """Try to open browser"""
        import webbrowser
        try:
            webbrowser.open("http://localhost:8000")
            print("🌐 Opened browser to dashboard")
        except Exception as e:
            print(f"Could not open browser: {e}")
        input("\nPress Enter to continue...")
        
    def show_help(self):
        """Show help information"""
        print("\n📚 HELP:")
        print("This monitor shows your automated revenue system in real-time")
        print("- Revenue updates every 30 seconds automatically")
        print("- All 5 revenue streams are tracked")
        print("- Use commands to interact with the system")
        print("- The web dashboard is at: http://localhost:8000")
        input("\nPress Enter to continue...")
        
    def run_simple(self):
        """Run a simple one-time display"""
        self.clear_screen()
        self.print_header()
        
        revenue_data = self.get_revenue_data()
        status_data = self.get_status_data()
        
        self.print_revenue_summary(revenue_data)
        self.print_system_status(status_data)
        
        if "total_revenue_today" in revenue_data:
            self.print_growth_indicator(revenue_data["total_revenue_today"])

def main():
    monitor = RevenueMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--simple":
        monitor.run_simple()
    else:
        monitor.run_interactive()

if __name__ == "__main__":
    main()
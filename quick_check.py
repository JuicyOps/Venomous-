#!/usr/bin/env python3
"""
💰 Quick Revenue Check - Simple One-Line Status
"""

import requests
import json
from datetime import datetime

def quick_check():
    """Quick revenue check"""
    try:
        # Get revenue data
        response = requests.get("http://localhost:8000/api/revenue/summary", timeout=3)
        data = response.json()
        
        total = data['total_revenue_today']
        monthly = data['projected_monthly']
        
        print(f"💰 REVENUE TODAY: ${total:,.2f}")
        print(f"📅 MONTHLY PROJECTION: ${monthly:,.2f}")
        print(f"🚀 STATUS: ALL SYSTEMS ACTIVE")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print("❌ REVENUE SYSTEM OFFLINE")
        print("🔧 Run: ./start_money_maker.sh")
        return False

if __name__ == "__main__":
    quick_check()
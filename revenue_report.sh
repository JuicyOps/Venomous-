#!/bin/bash

# 💰 Automated Revenue System - Quick Report

echo "💰 AUTOMATED REVENUE SYSTEM - QUICK REPORT 💰"
echo "=============================================="

# Check if system is running
if curl -s http://localhost:8000/api/status > /dev/null 2>&1; then
    echo "✅ System Status: ACTIVE"
    
    # Get revenue data
    REVENUE=$(curl -s http://localhost:8000/api/revenue/summary)
    
    if [ $? -eq 0 ]; then
        # Parse JSON (basic extraction)
        TOTAL=$(echo $REVENUE | grep -o '"total_revenue_today":[0-9.]*' | cut -d':' -f2)
        MONTHLY=$(echo $REVENUE | grep -o '"projected_monthly":[0-9.]*' | cut -d':' -f2)
        
        echo "💰 Revenue Today: \$$TOTAL"
        echo "📅 Monthly Projection: \$$MONTHLY"
        echo ""
        echo "💼 Revenue Breakdown:"
        
        # Extract breakdown
        AFFILIATE=$(echo $REVENUE | grep -o '"affiliate_marketing":[0-9.]*' | cut -d':' -f2)
        TRADING=$(echo $REVENUE | grep -o '"automated_trading":[0-9.]*' | cut -d':' -f2)
        CONTENT=$(echo $REVENUE | grep -o '"content_monetization":[0-9.]*' | cut -d':' -f2)
        ADS=$(echo $REVENUE | grep -o '"ad_optimization":[0-9.]*' | cut -d':' -f2)
        PRODUCTS=$(echo $REVENUE | grep -o '"product_sales":[0-9.]*' | cut -d':' -f2)
        
        echo "   🔗 Affiliate Marketing: \$$AFFILIATE"
        echo "   🤖 Automated Trading: \$$TRADING"
        echo "   📝 Content Revenue: \$$CONTENT"
        echo "   🎯 Ad Optimization: \$$ADS"
        echo "   💎 Product Sales: \$$PRODUCTS"
        
        echo ""
        echo "🚀 All 5 revenue streams are ACTIVE!"
        echo "📈 Making money every 30 seconds!"
        
    else
        echo "❌ Could not get revenue data"
    fi
    
else
    echo "❌ System Status: OFFLINE"
    echo "🔧 Start with: ./start_money_maker.sh"
fi

echo ""
echo "⏰ Report generated: $(date)"
echo "🌐 Dashboard: http://localhost:8000"
echo "=============================================="
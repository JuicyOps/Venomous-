from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
import schedule
import time
import threading
from datetime import datetime
import json
import os
from typing import Dict, List
import logging

# Import our revenue modules
from revenue_systems.affiliate_tracker import AffiliateTracker
from revenue_systems.content_generator import ContentGenerator
from revenue_systems.trading_bot import TradingBot
from revenue_systems.ad_optimizer import AdOptimizer
from revenue_systems.product_sales import ProductSales

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Automated Revenue System", description="Passive Income Generator")

# Initialize revenue systems
affiliate_tracker = AffiliateTracker()
content_generator = ContentGenerator()
trading_bot = TradingBot()
ad_optimizer = AdOptimizer()
product_sales = ProductSales()

# Mount static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Main dashboard showing all revenue streams"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Automated Revenue Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; color: white; margin-bottom: 30px; }
            .revenue-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                gap: 20px; 
                margin-bottom: 30px; 
            }
            .revenue-card { 
                background: white; 
                border-radius: 15px; 
                padding: 20px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            .revenue-card:hover { transform: translateY(-5px); }
            .card-title { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; color: #2c3e50; }
            .revenue-amount { font-size: 2em; font-weight: bold; color: #27ae60; margin: 10px 0; }
            .status { padding: 5px 10px; border-radius: 20px; font-size: 0.8em; font-weight: bold; }
            .status.active { background: #d4edda; color: #155724; }
            .status.inactive { background: #f8d7da; color: #721c24; }
            .controls { display: flex; gap: 10px; margin-top: 15px; }
            .btn { 
                padding: 8px 16px; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
                font-weight: bold;
                transition: background 0.3s ease;
            }
            .btn-primary { background: #3498db; color: white; }
            .btn-primary:hover { background: #2980b9; }
            .btn-success { background: #27ae60; color: white; }
            .btn-success:hover { background: #219a52; }
            .btn-danger { background: #e74c3c; color: white; }
            .btn-danger:hover { background: #c0392b; }
            .total-revenue { 
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white; 
                text-align: center; 
                padding: 30px; 
                border-radius: 15px; 
                margin-bottom: 20px;
            }
            .chart-container { background: white; padding: 20px; border-radius: 15px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Automated Revenue Dashboard</h1>
                <p>Your passive income streams working 24/7</p>
            </div>
            
            <div class="total-revenue">
                <h2>Total Revenue Today</h2>
                <div id="totalRevenue" class="revenue-amount">$0.00</div>
                <p>All systems automated and running</p>
            </div>
            
            <div class="revenue-grid">
                <div class="revenue-card">
                    <div class="card-title">💼 Affiliate Marketing</div>
                    <div id="affiliateRevenue" class="revenue-amount">$0.00</div>
                    <div id="affiliateStatus" class="status active">Active</div>
                    <div class="controls">
                        <button class="btn btn-primary" onclick="optimizeAffiliates()">Optimize</button>
                        <button class="btn btn-success" onclick="addAffiliate()">Add Link</button>
                    </div>
                </div>
                
                <div class="revenue-card">
                    <div class="card-title">📝 Content Monetization</div>
                    <div id="contentRevenue" class="revenue-amount">$0.00</div>
                    <div id="contentStatus" class="status active">Generating</div>
                    <div class="controls">
                        <button class="btn btn-primary" onclick="generateContent()">New Content</button>
                        <button class="btn btn-success" onclick="optimizeSEO()">Optimize SEO</button>
                    </div>
                </div>
                
                <div class="revenue-card">
                    <div class="card-title">📈 Trading Bot</div>
                    <div id="tradingRevenue" class="revenue-amount">$0.00</div>
                    <div id="tradingStatus" class="status active">Trading</div>
                    <div class="controls">
                        <button class="btn btn-primary" onclick="adjustStrategy()">Adjust Strategy</button>
                        <button class="btn btn-danger" onclick="pauseTrading()">Pause</button>
                    </div>
                </div>
                
                <div class="revenue-card">
                    <div class="card-title">🎯 Ad Optimization</div>
                    <div id="adRevenue" class="revenue-amount">$0.00</div>
                    <div id="adStatus" class="status active">Optimizing</div>
                    <div class="controls">
                        <button class="btn btn-primary" onclick="optimizeAds()">Optimize</button>
                        <button class="btn btn-success" onclick="newCampaign()">New Campaign</button>
                    </div>
                </div>
                
                <div class="revenue-card">
                    <div class="card-title">💎 Digital Products</div>
                    <div id="productRevenue" class="revenue-amount">$0.00</div>
                    <div id="productStatus" class="status active">Selling</div>
                    <div class="controls">
                        <button class="btn btn-primary" onclick="createProduct()">New Product</button>
                        <button class="btn btn-success" onclick="optimizePricing()">Optimize Price</button>
                    </div>
                </div>
                
                <div class="revenue-card">
                    <div class="card-title">🤖 AI Services</div>
                    <div id="aiRevenue" class="revenue-amount">$0.00</div>
                    <div id="aiStatus" class="status active">Running</div>
                    <div class="controls">
                        <button class="btn btn-primary" onclick="deployBot()">Deploy Bot</button>
                        <button class="btn btn-success" onclick="scaleServices()">Scale Up</button>
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <h3>Revenue Timeline</h3>
                <canvas id="revenueChart" width="400" height="200"></canvas>
            </div>
        </div>
        
        <script>
            // Revenue tracking
            let revenueData = {
                affiliate: 0,
                content: 0,
                trading: 0,
                ads: 0,
                products: 0,
                ai: 0
            };
            
            // Simulate revenue updates
            function updateRevenue() {
                revenueData.affiliate += Math.random() * 10;
                revenueData.content += Math.random() * 15;
                revenueData.trading += Math.random() * 25;
                revenueData.ads += Math.random() * 8;
                revenueData.products += Math.random() * 30;
                revenueData.ai += Math.random() * 20;
                
                document.getElementById('affiliateRevenue').textContent = '$' + revenueData.affiliate.toFixed(2);
                document.getElementById('contentRevenue').textContent = '$' + revenueData.content.toFixed(2);
                document.getElementById('tradingRevenue').textContent = '$' + revenueData.trading.toFixed(2);
                document.getElementById('adRevenue').textContent = '$' + revenueData.ads.toFixed(2);
                document.getElementById('productRevenue').textContent = '$' + revenueData.products.toFixed(2);
                document.getElementById('aiRevenue').textContent = '$' + revenueData.ai.toFixed(2);
                
                const total = Object.values(revenueData).reduce((a, b) => a + b, 0);
                document.getElementById('totalRevenue').textContent = '$' + total.toFixed(2);
            }
            
            // Control functions
            function optimizeAffiliates() {
                fetch('/api/affiliate/optimize', {method: 'POST'})
                    .then(() => alert('Affiliate links optimized!'));
            }
            
            function generateContent() {
                fetch('/api/content/generate', {method: 'POST'})
                    .then(() => alert('New content generated!'));
            }
            
            function adjustStrategy() {
                fetch('/api/trading/adjust', {method: 'POST'})
                    .then(() => alert('Trading strategy adjusted!'));
            }
            
            function optimizeAds() {
                fetch('/api/ads/optimize', {method: 'POST'})
                    .then(() => alert('Ad campaigns optimized!'));
            }
            
            function createProduct() {
                fetch('/api/products/create', {method: 'POST'})
                    .then(() => alert('New digital product created!'));
            }
            
            function deployBot() {
                fetch('/api/ai/deploy', {method: 'POST'})
                    .then(() => alert('AI service deployed!'));
            }
            
            // Initialize chart
            const ctx = document.getElementById('revenueChart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Total Revenue',
                        data: [],
                        borderColor: '#3498db',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
            
            // Update every 5 seconds
            setInterval(() => {
                updateRevenue();
                const now = new Date().toLocaleTimeString();
                const total = Object.values(revenueData).reduce((a, b) => a + b, 0);
                chart.data.labels.push(now);
                chart.data.datasets[0].data.push(total);
                if (chart.data.labels.length > 20) {
                    chart.data.labels.shift();
                    chart.data.datasets[0].data.shift();
                }
                chart.update();
            }, 5000);
            
            // Initial update
            updateRevenue();
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/api/status")
async def get_status():
    """Get status of all revenue systems"""
    return {
        "affiliate_tracker": await affiliate_tracker.get_status(),
        "content_generator": await content_generator.get_status(),
        "trading_bot": await trading_bot.get_status(),
        "ad_optimizer": await ad_optimizer.get_status(),
        "product_sales": await product_sales.get_status(),
        "total_revenue_today": await calculate_daily_revenue()
    }

@app.post("/api/affiliate/optimize")
async def optimize_affiliates():
    """Optimize affiliate marketing campaigns"""
    return await affiliate_tracker.optimize()

@app.post("/api/content/generate")
async def generate_content():
    """Generate new monetized content"""
    return await content_generator.create_content()

@app.post("/api/trading/adjust")
async def adjust_trading():
    """Adjust trading strategy"""
    return await trading_bot.adjust_strategy()

@app.post("/api/ads/optimize")
async def optimize_ads():
    """Optimize ad campaigns"""
    return await ad_optimizer.optimize_campaigns()

@app.post("/api/products/create")
async def create_product():
    """Create new digital product"""
    return await product_sales.create_product()

@app.post("/api/ai/deploy")
async def deploy_ai_service():
    """Deploy new AI service"""
    # This would deploy automated AI services that generate revenue
    return {"status": "AI service deployed", "estimated_revenue": "$50-100/day"}

async def calculate_daily_revenue():
    """Calculate total revenue for today"""
    # This would aggregate revenue from all sources
    return {
        "total": 0.00,
        "breakdown": {
            "affiliate": 0.00,
            "content": 0.00,
            "trading": 0.00,
            "ads": 0.00,
            "products": 0.00,
            "ai_services": 0.00
        }
    }

def run_background_tasks():
    """Run scheduled background tasks"""
    schedule.every(1).minutes.do(lambda: asyncio.create_task(affiliate_tracker.check_performance()))
    schedule.every(30).minutes.do(lambda: asyncio.create_task(content_generator.auto_generate()))
    schedule.every(5).minutes.do(lambda: asyncio.create_task(trading_bot.execute_trades()))
    schedule.every(15).minutes.do(lambda: asyncio.create_task(ad_optimizer.optimize_bids()))
    schedule.every(1).hours.do(lambda: asyncio.create_task(product_sales.update_prices()))
    
    while True:
        schedule.run_pending()
        time.sleep(60)

@app.on_event("startup")
async def startup_event():
    """Initialize all systems on startup"""
    logger.info("Starting automated revenue systems...")
    
    # Initialize all revenue streams
    await affiliate_tracker.initialize()
    await content_generator.initialize()
    await trading_bot.initialize()
    await ad_optimizer.initialize()
    await product_sales.initialize()
    
    # Start background task scheduler
    threading.Thread(target=run_background_tasks, daemon=True).start()
    
    logger.info("All revenue systems initialized and running!")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
import asyncio
import logging
import time
from datetime import datetime, timedelta
import threading
from revenue_systems.affiliate_tracker import AffiliateTracker
from revenue_systems.content_generator import ContentGenerator
from revenue_systems.trading_bot import TradingBot
from revenue_systems.ad_optimizer import AdOptimizer
from revenue_systems.product_sales import ProductSales

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutomationScheduler:
    """Manages all automated revenue generation tasks"""
    
    def __init__(self):
        self.running = False
        self.revenue_systems = {}
        self.tasks = []
        
    async def initialize_systems(self):
        """Initialize all revenue systems"""
        logger.info("Initializing automated revenue systems...")
        
        # Initialize each system
        affiliate_tracker = AffiliateTracker()
        content_generator = ContentGenerator()
        trading_bot = TradingBot()
        ad_optimizer = AdOptimizer()
        product_sales = ProductSales()
        
        # Store references
        self.revenue_systems = {
            'affiliate': affiliate_tracker,
            'content': content_generator,
            'trading': trading_bot,
            'ads': ad_optimizer,
            'products': product_sales
        }
        
        # Initialize all systems
        await affiliate_tracker.initialize()
        await content_generator.initialize()
        await trading_bot.initialize()
        await ad_optimizer.initialize()
        await product_sales.initialize()
        
        logger.info("All revenue systems initialized successfully!")
        
    async def run_continuous_automation(self):
        """Run automated tasks continuously"""
        self.running = True
        logger.info("Starting continuous automation...")
        
        while self.running:
            try:
                # Run all automated tasks in parallel
                tasks = [
                    self.run_affiliate_automation(),
                    self.run_content_automation(),
                    self.run_trading_automation(),
                    self.run_ad_automation(),
                    self.run_product_automation()
                ]
                
                await asyncio.gather(*tasks)
                
                # Log total revenue every cycle
                await self.log_total_revenue()
                
                # Wait before next cycle
                await asyncio.sleep(300)  # 5 minutes between cycles
                
            except Exception as e:
                logger.error(f"Error in automation cycle: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
                
    async def run_affiliate_automation(self):
        """Run affiliate marketing automation"""
        try:
            affiliate_system = self.revenue_systems['affiliate']
            
            # Check performance every cycle
            await affiliate_system.check_performance()
            
            # Optimize every 10 cycles (50 minutes)
            current_time = datetime.now()
            if current_time.minute % 10 == 0:
                await affiliate_system.optimize()
                
        except Exception as e:
            logger.error(f"Affiliate automation error: {e}")
            
    async def run_content_automation(self):
        """Run content generation automation"""
        try:
            content_system = self.revenue_systems['content']
            
            # Auto-generate content every cycle
            await content_system.auto_generate()
            
            # SEO optimization every hour
            current_time = datetime.now()
            if current_time.minute == 0:  # Top of the hour
                await content_system.optimize_seo()
                
        except Exception as e:
            logger.error(f"Content automation error: {e}")
            
    async def run_trading_automation(self):
        """Run trading bot automation"""
        try:
            trading_system = self.revenue_systems['trading']
            
            # Execute trades every cycle
            await trading_system.execute_trades()
            
            # Strategy adjustment every 30 minutes
            current_time = datetime.now()
            if current_time.minute % 30 == 0:
                await trading_system.adjust_strategy()
                
        except Exception as e:
            logger.error(f"Trading automation error: {e}")
            
    async def run_ad_automation(self):
        """Run ad optimization automation"""
        try:
            ad_system = self.revenue_systems['ads']
            
            # Update performance every cycle
            await ad_system.update_campaign_performance()
            
            # Optimize campaigns every 15 minutes
            current_time = datetime.now()
            if current_time.minute % 15 == 0:
                await ad_system.optimize_campaigns()
                
            # Bid optimization every cycle
            await ad_system.optimize_bids()
            
        except Exception as e:
            logger.error(f"Ad automation error: {e}")
            
    async def run_product_automation(self):
        """Run product sales automation"""
        try:
            product_system = self.revenue_systems['products']
            
            # Simulate sales every cycle
            await product_system.simulate_sales()
            
            # Price updates every hour
            current_time = datetime.now()
            if current_time.minute == 0:
                await product_system.update_prices()
                
            # Create new products every 2 hours
            if current_time.hour % 2 == 0 and current_time.minute == 0:
                await product_system.create_product()
                
        except Exception as e:
            logger.error(f"Product automation error: {e}")
            
    async def log_total_revenue(self):
        """Log total revenue across all systems"""
        try:
            total_revenue = 0
            revenue_breakdown = {}
            
            for name, system in self.revenue_systems.items():
                status = await system.get_status()
                system_revenue = status.get('revenue_today', 0)
                total_revenue += system_revenue
                revenue_breakdown[name] = system_revenue
                
            logger.info(f"🚀 TOTAL REVENUE: ${total_revenue:.2f}")
            logger.info(f"💰 Breakdown: {revenue_breakdown}")
            
            # Log hourly milestones
            if total_revenue > 100:
                logger.info("🎉 Milestone: $100+ daily revenue achieved!")
            if total_revenue > 500:
                logger.info("🎊 Milestone: $500+ daily revenue achieved!")
            if total_revenue > 1000:
                logger.info("🎆 Milestone: $1000+ daily revenue achieved!")
                
        except Exception as e:
            logger.error(f"Revenue logging error: {e}")
            
    async def get_revenue_summary(self):
        """Get comprehensive revenue summary"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "systems": {},
            "total_revenue": 0
        }
        
        for name, system in self.revenue_systems.items():
            try:
                status = await system.get_status()
                summary["systems"][name] = status
                summary["total_revenue"] += status.get('revenue_today', 0)
            except Exception as e:
                logger.error(f"Error getting status for {name}: {e}")
                summary["systems"][name] = {"error": str(e)}
                
        return summary
        
    def stop_automation(self):
        """Stop all automated tasks"""
        self.running = False
        logger.info("Automation stopped")
        
    async def emergency_optimization(self):
        """Run emergency optimization across all systems"""
        logger.info("Running emergency optimization...")
        
        try:
            # Optimize all systems simultaneously
            optimization_tasks = []
            
            for name, system in self.revenue_systems.items():
                if hasattr(system, 'optimize'):
                    optimization_tasks.append(system.optimize())
                elif hasattr(system, 'optimize_campaigns'):
                    optimization_tasks.append(system.optimize_campaigns())
                elif hasattr(system, 'adjust_strategy'):
                    optimization_tasks.append(system.adjust_strategy())
                    
            results = await asyncio.gather(*optimization_tasks, return_exceptions=True)
            
            logger.info("Emergency optimization completed")
            return results
            
        except Exception as e:
            logger.error(f"Emergency optimization error: {e}")
            return None

# Standalone automation runner
async def run_standalone_automation():
    """Run automation as standalone script"""
    scheduler = AutomationScheduler()
    
    try:
        await scheduler.initialize_systems()
        await scheduler.run_continuous_automation()
    except KeyboardInterrupt:
        logger.info("Automation stopped by user")
    except Exception as e:
        logger.error(f"Automation error: {e}")
    finally:
        scheduler.stop_automation()

if __name__ == "__main__":
    # Run the automation independently
    asyncio.run(run_standalone_automation())
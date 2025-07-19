import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class AdOptimizer:
    """Automated advertising campaign optimizer"""
    
    def __init__(self):
        self.campaigns = []
        self.revenue_today = 0.0
        self.status = "inactive"
        self.ad_networks = ["Google Ads", "Facebook Ads", "TikTok Ads", "LinkedIn Ads"]
        
    async def initialize(self):
        """Initialize the ad optimization system"""
        self.status = "active"
        
        # Create initial campaigns
        campaign_types = [
            {"name": "Tech Reviews Display", "type": "Display", "network": "Google Ads"},
            {"name": "Finance Content Video", "type": "Video", "network": "YouTube"},
            {"name": "Business Tools Social", "type": "Social", "network": "Facebook Ads"},
            {"name": "Course Promotion Search", "type": "Search", "network": "Google Ads"}
        ]
        
        for i, campaign_info in enumerate(campaign_types):
            campaign = {
                "id": f"campaign_{i}",
                "name": campaign_info["name"],
                "type": campaign_info["type"],
                "network": campaign_info["network"],
                "budget_daily": random.uniform(20, 100),
                "spend_today": 0.0,
                "impressions": 0,
                "clicks": 0,
                "conversions": 0,
                "revenue": 0.0,
                "ctr": 0.0,
                "cpc": 0.0,
                "roas": 0.0,
                "status": "active",
                "created_at": datetime.now().isoformat()
            }
            
            self.campaigns.append(campaign)
            
        logger.info("Ad optimizer initialized with {} campaigns".format(len(self.campaigns)))
        
    async def get_status(self):
        """Get current status and performance metrics"""
        total_spend = sum(campaign["spend_today"] for campaign in self.campaigns)
        total_revenue = sum(campaign["revenue"] for campaign in self.campaigns)
        total_impressions = sum(campaign["impressions"] for campaign in self.campaigns)
        total_clicks = sum(campaign["clicks"] for campaign in self.campaigns)
        
        return {
            "status": self.status,
            "total_campaigns": len(self.campaigns),
            "active_campaigns": len([c for c in self.campaigns if c["status"] == "active"]),
            "total_spend": total_spend,
            "total_revenue": total_revenue,
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "overall_roas": (total_revenue / max(total_spend, 1)),
            "overall_ctr": (total_clicks / max(total_impressions, 1)) * 100
        }
        
    async def update_campaign_performance(self):
        """Update performance metrics for all campaigns"""
        for campaign in self.campaigns:
            if campaign["status"] != "active":
                continue
                
            # Simulate performance data
            daily_budget = campaign["budget_daily"]
            spend_rate = random.uniform(0.7, 1.2)  # May spend 70-120% of budget
            spend_today = min(daily_budget * spend_rate, daily_budget * 1.5)
            
            # Calculate impressions based on spend and CPM
            cpm = random.uniform(2, 8)  # Cost per 1000 impressions
            new_impressions = int((spend_today / cpm) * 1000)
            
            # Calculate clicks based on CTR
            base_ctr = 0.02 if campaign["type"] == "Search" else 0.01
            ctr = random.uniform(base_ctr * 0.5, base_ctr * 2)
            new_clicks = int(new_impressions * ctr)
            
            # Calculate conversions
            conversion_rate = random.uniform(0.01, 0.05)  # 1-5% conversion rate
            new_conversions = int(new_clicks * conversion_rate)
            
            # Calculate revenue
            avg_order_value = random.uniform(50, 300)
            new_revenue = new_conversions * avg_order_value
            
            # Update campaign metrics
            campaign["spend_today"] += spend_today
            campaign["impressions"] += new_impressions
            campaign["clicks"] += new_clicks
            campaign["conversions"] += new_conversions
            campaign["revenue"] += new_revenue
            
            # Calculate derived metrics
            campaign["ctr"] = (campaign["clicks"] / max(campaign["impressions"], 1)) * 100
            campaign["cpc"] = campaign["spend_today"] / max(campaign["clicks"], 1)
            campaign["roas"] = campaign["revenue"] / max(campaign["spend_today"], 1)
            
        # Update total revenue
        self.revenue_today = sum(campaign["revenue"] for campaign in self.campaigns)
        
        logger.info(f"Updated ad performance. Total revenue: ${self.revenue_today:.2f}")
        
    async def optimize_campaigns(self):
        """Optimize campaign performance automatically"""
        await self.update_campaign_performance()
        
        optimizations = []
        
        for campaign in self.campaigns:
            if campaign["status"] != "active":
                continue
                
            # Optimization strategies based on performance
            if campaign["roas"] < 1.5:  # Low ROAS
                # Reduce budget or pause
                if campaign["roas"] < 0.8:
                    campaign["status"] = "paused"
                    optimizations.append(f"Paused {campaign['name']} due to low ROAS")
                else:
                    campaign["budget_daily"] *= 0.8  # Reduce budget by 20%
                    optimizations.append(f"Reduced budget for {campaign['name']}")
                    
            elif campaign["roas"] > 3.0:  # High ROAS
                # Increase budget
                campaign["budget_daily"] *= 1.3  # Increase budget by 30%
                optimizations.append(f"Increased budget for {campaign['name']}")
                
            if campaign["ctr"] < 0.5:  # Very low CTR
                # Simulate ad creative refresh
                campaign["ctr"] *= 1.5  # Improve CTR with better creatives
                optimizations.append(f"Refreshed creatives for {campaign['name']}")
                
        logger.info(f"Completed campaign optimization with {len(optimizations)} changes")
        
        return {
            "status": "optimized",
            "optimizations": optimizations,
            "estimated_improvement": "10-25% performance increase"
        }
        
    async def optimize_bids(self):
        """Automatically optimize bid strategies"""
        if self.status != "active":
            return
            
        for campaign in self.campaigns:
            if campaign["status"] != "active":
                continue
                
            # Simulate bid optimization
            current_cpc = campaign["cpc"]
            target_cpc = random.uniform(0.5, 3.0)
            
            if current_cpc > target_cpc * 1.2:
                # Bids too high, reduce
                campaign["cpc"] *= 0.9
            elif current_cpc < target_cpc * 0.8:
                # Bids too low, increase
                campaign["cpc"] *= 1.1
                
        logger.info("Automated bid optimization completed")
        
    async def create_new_campaign(self, campaign_data: Dict):
        """Create a new advertising campaign"""
        campaign = {
            "id": f"campaign_{len(self.campaigns)}",
            "name": campaign_data.get("name", f"Campaign {len(self.campaigns)}"),
            "type": campaign_data.get("type", "Display"),
            "network": campaign_data.get("network", "Google Ads"),
            "budget_daily": campaign_data.get("budget", 50.0),
            "spend_today": 0.0,
            "impressions": 0,
            "clicks": 0,
            "conversions": 0,
            "revenue": 0.0,
            "ctr": 0.0,
            "cpc": 0.0,
            "roas": 0.0,
            "status": "active",
            "created_at": datetime.now().isoformat()
        }
        
        self.campaigns.append(campaign)
        logger.info(f"Created new campaign: {campaign['name']}")
        
        return {"status": "created", "campaign": campaign}
        
    async def get_top_campaigns(self):
        """Get top performing campaigns"""
        active_campaigns = [c for c in self.campaigns if c["status"] == "active"]
        return sorted(active_campaigns, key=lambda x: x["roas"], reverse=True)[:5]
        
    async def pause_campaign(self, campaign_id: str):
        """Pause a specific campaign"""
        for campaign in self.campaigns:
            if campaign["id"] == campaign_id:
                campaign["status"] = "paused"
                logger.info(f"Paused campaign: {campaign['name']}")
                return {"status": "paused", "campaign_id": campaign_id}
                
        return {"status": "error", "message": "Campaign not found"}
        
    async def resume_campaign(self, campaign_id: str):
        """Resume a paused campaign"""
        for campaign in self.campaigns:
            if campaign["id"] == campaign_id:
                campaign["status"] = "active"
                logger.info(f"Resumed campaign: {campaign['name']}")
                return {"status": "resumed", "campaign_id": campaign_id}
                
        return {"status": "error", "message": "Campaign not found"}
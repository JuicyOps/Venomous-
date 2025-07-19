import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class ProductSales:
    """Automated digital product creation and sales system"""
    
    def __init__(self):
        self.products = []
        self.sales_today = []
        self.revenue_today = 0.0
        self.status = "inactive"
        self.product_categories = [
            "Online Courses",
            "E-books",
            "Software Tools",
            "Templates",
            "Digital Art",
            "Music/Audio",
            "Video Content",
            "Mobile Apps"
        ]
        
    async def initialize(self):
        """Initialize the product sales system"""
        self.status = "active"
        
        # Create initial digital products
        initial_products = [
            {
                "name": "Complete Digital Marketing Course",
                "category": "Online Courses",
                "price": 97.00,
                "cost": 5.00,
                "description": "Learn digital marketing from scratch"
            },
            {
                "name": "Business Plan Templates Pack",
                "category": "Templates",
                "price": 29.99,
                "cost": 2.00,
                "description": "Professional business plan templates"
            },
            {
                "name": "Cryptocurrency Investment Guide",
                "category": "E-books",
                "price": 19.99,
                "cost": 1.00,
                "description": "Complete guide to crypto investing"
            },
            {
                "name": "Social Media Graphics Bundle",
                "category": "Digital Art",
                "price": 39.99,
                "cost": 3.00,
                "description": "1000+ social media graphics"
            },
            {
                "name": "Productivity Apps Suite",
                "category": "Software Tools",
                "price": 79.99,
                "cost": 10.00,
                "description": "5 productivity apps bundle"
            }
        ]
        
        for product_data in initial_products:
            await self.create_product_internal(product_data)
            
        logger.info("Product sales system initialized with {} products".format(len(self.products)))
        
    async def get_status(self):
        """Get current status and sales metrics"""
        total_sales = len(self.sales_today)
        total_revenue = sum(sale["price"] for sale in self.sales_today)
        total_profit = sum(sale["profit"] for sale in self.sales_today)
        
        active_products = [p for p in self.products if p["status"] == "active"]
        
        return {
            "status": self.status,
            "total_products": len(self.products),
            "active_products": len(active_products),
            "sales_today": total_sales,
            "revenue_today": total_revenue,
            "profit_today": total_profit,
            "avg_order_value": total_revenue / max(total_sales, 1),
            "conversion_rate": random.uniform(2, 8)  # Simulated conversion rate
        }
        
    async def create_product_internal(self, product_data: Dict):
        """Internal method to create a product"""
        product = {
            "id": f"product_{len(self.products)}",
            "name": product_data["name"],
            "category": product_data["category"],
            "price": product_data["price"],
            "cost": product_data.get("cost", 0.0),
            "description": product_data["description"],
            "sales_count": 0,
            "revenue_total": 0.0,
            "rating": random.uniform(4.0, 4.9),
            "reviews_count": random.randint(10, 500),
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "last_sale": None
        }
        
        self.products.append(product)
        return product
        
    async def simulate_sales(self):
        """Simulate automated sales"""
        if self.status != "active":
            return
            
        active_products = [p for p in self.products if p["status"] == "active"]
        
        for product in active_products:
            # Simulate sales probability based on product category and price
            base_sales_prob = 0.3  # 30% chance per update cycle
            
            # Adjust probability based on price (lower price = higher sales probability)
            price_factor = max(0.1, 1.0 - (product["price"] / 200.0))
            
            # Adjust based on category popularity
            category_multipliers = {
                "Online Courses": 1.2,
                "E-books": 1.0,
                "Templates": 1.1,
                "Software Tools": 0.9,
                "Digital Art": 0.8,
                "Music/Audio": 0.7,
                "Video Content": 1.0,
                "Mobile Apps": 0.9
            }
            
            category_factor = category_multipliers.get(product["category"], 1.0)
            
            # Calculate final sales probability
            sales_prob = base_sales_prob * price_factor * category_factor
            
            # Simulate multiple sales
            sales_count = 0
            for _ in range(random.randint(1, 5)):  # Check up to 5 potential sales
                if random.random() < sales_prob:
                    sales_count += 1
                    
            # Record sales
            for _ in range(sales_count):
                sale = {
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "price": product["price"],
                    "cost": product["cost"],
                    "profit": product["price"] - product["cost"],
                    "timestamp": datetime.now().isoformat(),
                    "customer_country": random.choice(["US", "UK", "CA", "AU", "DE", "FR", "ES"])
                }
                
                self.sales_today.append(sale)
                
                # Update product metrics
                product["sales_count"] += 1
                product["revenue_total"] += product["price"]
                product["last_sale"] = sale["timestamp"]
                
        # Update total revenue
        self.revenue_today = sum(sale["price"] for sale in self.sales_today)
        
        if len(self.sales_today) > 0:
            logger.info(f"Generated {len(self.sales_today)} sales totaling ${self.revenue_today:.2f}")
            
    async def create_product(self):
        """Create a new digital product"""
        # Generate product idea
        category = random.choice(self.product_categories)
        
        product_ideas = {
            "Online Courses": [
                "AI & Machine Learning Mastery",
                "Blockchain Development Bootcamp",
                "Social Media Marketing Pro",
                "Python Programming Complete"
            ],
            "E-books": [
                "Passive Income Strategies",
                "Cryptocurrency Trading Guide",
                "Remote Work Success",
                "Personal Finance Mastery"
            ],
            "Templates": [
                "Website Design Templates",
                "Email Marketing Templates",
                "Resume & CV Templates",
                "Presentation Templates"
            ],
            "Software Tools": [
                "SEO Analysis Tool",
                "Social Media Scheduler",
                "Project Management App",
                "Invoice Generator"
            ]
        }
        
        name = random.choice(product_ideas.get(category, ["Generic Digital Product"]))
        
        # Price based on category
        price_ranges = {
            "Online Courses": (49, 199),
            "E-books": (9, 39),
            "Templates": (19, 59),
            "Software Tools": (29, 149),
            "Digital Art": (9, 49),
            "Music/Audio": (5, 29),
            "Video Content": (19, 99),
            "Mobile Apps": (0.99, 9.99)
        }
        
        price_range = price_ranges.get(category, (10, 50))
        price = round(random.uniform(price_range[0], price_range[1]), 2)
        cost = round(price * random.uniform(0.05, 0.15), 2)  # 5-15% of price
        
        product_data = {
            "name": name,
            "category": category,
            "price": price,
            "cost": cost,
            "description": f"High-quality {category.lower()} for professionals"
        }
        
        product = await self.create_product_internal(product_data)
        
        logger.info(f"Created new product: {name} for ${price}")
        
        return {
            "status": "created",
            "product": product,
            "estimated_sales": "5-20/day"
        }
        
    async def update_prices(self):
        """Dynamically update product prices based on performance"""
        for product in self.products:
            if product["status"] != "active":
                continue
                
            # Simple price optimization logic
            sales_velocity = product["sales_count"]  # Sales since creation
            
            if sales_velocity > 50:  # High demand
                # Increase price by up to 10%
                price_increase = random.uniform(1.0, 1.1)
                product["price"] = round(product["price"] * price_increase, 2)
                
            elif sales_velocity < 5:  # Low demand
                # Decrease price by up to 15%
                price_decrease = random.uniform(0.85, 1.0)
                product["price"] = round(product["price"] * price_decrease, 2)
                
        logger.info("Product prices updated based on performance")
        
    async def get_top_products(self):
        """Get top selling products"""
        return sorted(self.products, key=lambda x: x["revenue_total"], reverse=True)[:5]
        
    async def optimize_pricing(self):
        """Optimize product pricing strategies"""
        optimizations = []
        
        for product in self.products:
            if product["status"] != "active":
                continue
                
            # A/B test pricing
            current_price = product["price"]
            
            # Test different pricing strategies
            if product["category"] == "E-books":
                # E-books perform better at lower prices
                if current_price > 25:
                    product["price"] = round(current_price * 0.9, 2)
                    optimizations.append(f"Reduced {product['name']} price for better conversion")
                    
            elif product["category"] == "Online Courses":
                # Courses can handle premium pricing
                if current_price < 80 and product["sales_count"] > 20:
                    product["price"] = round(current_price * 1.15, 2)
                    optimizations.append(f"Increased {product['name']} price due to high demand")
                    
        logger.info(f"Pricing optimization completed with {len(optimizations)} changes")
        
        return {
            "status": "optimized",
            "optimizations": optimizations,
            "estimated_revenue_increase": "8-20%"
        }
        
    async def get_sales_analytics(self):
        """Get detailed sales analytics"""
        if not self.sales_today:
            return {"message": "No sales data available"}
            
        # Revenue by category
        category_revenue = {}
        for sale in self.sales_today:
            product = next((p for p in self.products if p["id"] == sale["product_id"]), None)
            if product:
                category = product["category"]
                category_revenue[category] = category_revenue.get(category, 0) + sale["price"]
                
        # Top selling products
        product_sales = {}
        for sale in self.sales_today:
            product_id = sale["product_id"]
            product_sales[product_id] = product_sales.get(product_id, 0) + 1
            
        return {
            "total_sales": len(self.sales_today),
            "total_revenue": self.revenue_today,
            "category_breakdown": category_revenue,
            "top_products": dict(sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5])
        }
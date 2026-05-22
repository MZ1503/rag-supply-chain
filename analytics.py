import logging
import pandas as pd

logger = logging.getLogger(__name__)

# expected columns — if any missing, we catch it early
REQUIRED_COLUMNS = {
    'DAYS_TO_EXPIRY',
    'BRAND',
    'CATEGORY',
    'ACTUAL_QTY',
    'UNIT_PRICE_AED'
}


class Inventory:
    """
    Loads inventory CSV and pre-calculates all analytics metrics.
    
    Pre-calculation pattern chosen over Pandas Agent because:
    - 10,000+ rows caused LLM context issues on free tier
    - Known fixed questions benefit from exact pre-calculated answers
    - Faster response time — no LLM needed for calculations
    """

    def __init__(self, csv_path: str) -> None:
        """
        Loads CSV and calculates all metrics on startup.
        
        Args:
            csv_path: Path to inventory CSV file
            
        Raises:
            FileNotFoundError: If CSV file does not exist
            ValueError: If required columns are missing
        """
        # load CSV
        self.df = pd.read_csv(csv_path)
        logger.info(f"CSV loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")

        # Edge case 1 — validate required columns exist
        missing_cols = REQUIRED_COLUMNS - set(self.df.columns)
        if missing_cols:
            raise ValueError(f"CSV missing required columns: {missing_cols}")

        # Edge case 2 — warn about null values but do not crash
        null_counts = self.df.isnull().sum()
        if null_counts.any():
            logger.warning(f"Null values found:\n{null_counts[null_counts > 0]}")

        # calculate REVENUE once here so all metrics can use it
        self.df['REVENUE'] = self.df['ACTUAL_QTY'] * self.df['UNIT_PRICE_AED']
        logger.info("Revenue column calculated")

        # pre-calculate all metrics on startup
        self.metrics = self._calculate_metrics()
        logger.info("All metrics pre-calculated successfully")

    def _calculate_metrics(self) -> dict:
        """
        Pre-calculates all 10 inventory metrics.
        Called once on startup — results stored in self.metrics.
        
        Returns:
            Dictionary with 10 pre-calculated metric keys
        """
        # 1. How many products are expired?
        expired = self.df[self.df['DAYS_TO_EXPIRY'] < 0]

        # 2. Products expiring in next 7 days
        expiring_7_days = self.df[
            (self.df['DAYS_TO_EXPIRY'] > 0) &
            (self.df['DAYS_TO_EXPIRY'] < 7)
        ]

        # 3. Brand with most expired products
        # Edge case — what if no expired products exist?
        expired_by_brand = self.df[self.df['DAYS_TO_EXPIRY'] < 0].groupby('BRAND').size()
        top_expired_brand = expired_by_brand.idxmax() if not expired_by_brand.empty else "None"

        # 4. Brand with highest revenue
        top_revenue_brand = self.df.groupby('BRAND')['REVENUE'].sum().idxmax()

        # 5. Total inventory value
        total_inv_val = round(self.df['REVENUE'].sum(), 2)

        # 6. Category with most stock
        highest_stock_category = self.df.groupby('CATEGORY')['ACTUAL_QTY'].sum().idxmax()

        # 7. Products with zero stock
        products_zero_stock = self.df[self.df['ACTUAL_QTY'] == 0]

        # 8. Expiry rate by brand (percentage of expired products per brand)
        # why dict? — api.py can access by brand name, not by index position
        total_per_brand = self.df.groupby('BRAND').size()
        expired_per_brand = self.df[
            self.df['DAYS_TO_EXPIRY'] < 0
        ].groupby('BRAND').size()
        expiry_rate = (expired_per_brand / total_per_brand * 100).fillna(0).round(2)

        # 9. Brands needing urgent attention (expiry rate > 20%)
        urgent_brands = expiry_rate[expiry_rate > 20].index.tolist()

        # 10. Top 10 products by revenue
        # why dict? — preserves column names so api.py can access
        # p['BRAND'], p['REVENUE'] instead of p[0], p[1]
        top_10_products = (
            self.df.sort_values('REVENUE', ascending=False)
            .head(10)[['BRAND', 'CATEGORY', 'ACTUAL_QTY', 'REVENUE']]
        )

        return {
            "expired_count":          len(expired),
            "expiring_7_days":        expiring_7_days.to_dict('records'),
            "top_expired_brand":      top_expired_brand,
            "top_revenue_brand":      top_revenue_brand,
            "total_inv_val":          total_inv_val,
            "highest_stock_category": highest_stock_category,
            "products_zero_stock":    products_zero_stock.to_dict('records'),
            "expiry_rate_brand":      expiry_rate.to_dict(),
            "urgent_brands":          urgent_brands,
            "top_10_products":        top_10_products.to_dict('records')
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    inventory = Inventory("data/inventory_data.csv")
    print(inventory.metrics)
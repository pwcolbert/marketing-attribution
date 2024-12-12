import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def generate_customer_data(num_records=1000):
    """Generate sample customer demographic data"""
    age_ranges = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia']
    sources = ['Social Media', 'Search', 'Email', 'Referral', 'Direct', 'Paid Ads']
    
    data = {
        'customer_id': range(1, num_records + 1),
        'age_group': [random.choice(age_ranges) for _ in range(num_records)],
        'location': [random.choice(locations) for _ in range(num_records)],
        'acquisition_source': [random.choice(sources) for _ in range(num_records)],
        'signup_date': [
            (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
            for _ in range(num_records)
        ]
    }
    return pd.DataFrame(data)

def generate_campaign_data(num_campaigns=50):
    """Generate sample marketing campaign performance data"""
    campaign_types = ['Email', 'Social', 'Display', 'Search', 'Content']
    
    data = {
        'campaign_id': range(1, num_campaigns + 1),
        'campaign_name': [f'Campaign_{i}' for i in range(1, num_campaigns + 1)],
        'campaign_type': [random.choice(campaign_types) for _ in range(num_campaigns)],
        'start_date': [
            (datetime.now() - timedelta(days=random.randint(0, 180))).strftime('%Y-%m-%d')
            for _ in range(num_campaigns)
        ],
        'budget': [round(random.uniform(1000, 10000), 2) for _ in range(num_campaigns)],
        'impressions': [random.randint(10000, 1000000) for _ in range(num_campaigns)],
        'clicks': [random.randint(100, 50000) for _ in range(num_campaigns)],
        'conversions': [random.randint(10, 1000) for _ in range(num_campaigns)]
    }
    
    df = pd.DataFrame(data)
    df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
    df['conversion_rate'] = (df['conversions'] / df['clicks'] * 100).round(2)
    df['cpc'] = (df['budget'] / df['clicks']).round(2)
    df['cpa'] = (df['budget'] / df['conversions']).round(2)
    return df

def generate_engagement_data(customer_ids, num_records=5000):
    """Generate sample customer engagement events"""
    event_types = ['page_view', 'add_to_cart', 'purchase', 'email_open', 'email_click']
    
    data = {
        'event_id': range(1, num_records + 1),
        'customer_id': [random.choice(customer_ids) for _ in range(num_records)],
        'event_type': [random.choice(event_types) for _ in range(num_records)],
        'event_date': [
            (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
            for _ in range(num_records)
        ],
        'value': [
            round(random.uniform(0, 200), 2) if random.random() > 0.5 else 0
            for _ in range(num_records)
        ]
    }
    return pd.DataFrame(data)

def generate_purchase_data(customer_ids, num_records=3000):
    """Generate sample customer purchase data"""
    product_categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports', 'Beauty']
    payment_methods = ['Credit Card', 'PayPal', 'Debit Card', 'Gift Card']
    
    data = {
        'purchase_id': range(1, num_records + 1),
        'customer_id': [random.choice(customer_ids) for _ in range(num_records)],
        'purchase_date': [
            (datetime.now() - timedelta(days=random.randint(0, 180))).strftime('%Y-%m-%d')
            for _ in range(num_records)
        ],
        'product_category': [random.choice(product_categories) for _ in range(num_records)],
        'payment_method': [random.choice(payment_methods) for _ in range(num_records)],
        'purchase_amount': [round(random.uniform(10, 500), 2) for _ in range(num_records)],
        'items_quantity': [random.randint(1, 10) for _ in range(num_records)],
        'discount_applied': [random.choice([True, False]) for _ in range(num_records)],
        'discount_amount': [round(random.uniform(0, 50), 2) for _ in range(num_records)]
    }
    
    df = pd.DataFrame(data)
    # Set discount_amount to 0 where no discount was applied
    df.loc[~df['discount_applied'], 'discount_amount'] = 0
    return df

def generate_referral_data(customer_ids, num_records=1000):
    """Generate sample customer referral data"""
    referral_channels = ['Email Invite', 'Social Share', 'Personal Link', 'In-App Invite']
    status_options = ['Pending', 'Converted', 'Expired']
    
    data = {
        'referral_id': range(1, num_records + 1),
        'referrer_id': [random.choice(customer_ids) for _ in range(num_records)],
        'referral_date': [
            (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
            for _ in range(num_records)
        ],
        'referral_channel': [random.choice(referral_channels) for _ in range(num_records)],
        'status': [random.choice(status_options) for _ in range(num_records)],
        'referral_bonus': [
            round(random.uniform(10, 50), 2) if random.random() > 0.3 else 0
            for _ in range(num_records)
        ]
    }
    
    df = pd.DataFrame(data)
    # Add referred_customer_id only for converted referrals
    df['referred_customer_id'] = None
    converted_mask = df['status'] == 'Converted'
    df.loc[converted_mask, 'referred_customer_id'] = [
        random.choice(customer_ids) for _ in range(converted_mask.sum())
    ]
    return df

def generate_loyalty_data(customer_ids):
    """Generate sample customer loyalty and rewards data"""
    tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
    tier_benefits = {
        'Bronze': ['Basic Support', 'Birthday Reward'],
        'Silver': ['Priority Support', 'Free Shipping', 'Birthday Reward'],
        'Gold': ['Premium Support', 'Free Shipping', 'Birthday Reward', 'Early Access'],
        'Platinum': ['Concierge Support', 'Free Shipping', 'Birthday Reward', 'Early Access', 'VIP Events']
    }
    
    data = {
        'customer_id': customer_ids,
        'loyalty_points': [random.randint(0, 10000) for _ in range(len(customer_ids))],
        'tier': [random.choice(tiers) for _ in range(len(customer_ids))],
        'points_earned_ytd': [random.randint(0, 5000) for _ in range(len(customer_ids))],
        'points_redeemed_ytd': [random.randint(0, 3000) for _ in range(len(customer_ids))],
        'last_reward_date': [
            (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
            if random.random() > 0.3 else None
            for _ in range(len(customer_ids))
        ]
    }
    
    df = pd.DataFrame(data)
    # Add tier benefits based on tier
    df['tier_benefits'] = df['tier'].map(tier_benefits)
    # Calculate remaining points
    df['remaining_points'] = df['loyalty_points'] + df['points_earned_ytd'] - df['points_redeemed_ytd']
    return df

def calculate_rfm_scores(purchase_df, analysis_date=None):
    """
    Calculate RFM (Recency, Frequency, Monetary) scores for customers
    
    Parameters:
    purchase_df: DataFrame containing purchase data
    analysis_date: Optional reference date for recency calculation (defaults to latest purchase date)
    
    Returns:
    DataFrame with RFM scores and segments for each customer
    """
    # If no analysis date provided, use the latest purchase date plus one day
    if analysis_date is None:
        analysis_date = pd.to_datetime(purchase_df['purchase_date']).max() + timedelta(days=1)
    else:
        analysis_date = pd.to_datetime(analysis_date)
    
    # Convert purchase_date to datetime
    purchase_df['purchase_date'] = pd.to_datetime(purchase_df['purchase_date'])
    
    # Calculate RFM metrics
    rfm = purchase_df.groupby('customer_id').agg({
        'purchase_date': lambda x: (analysis_date - x.max()).days,  # Recency
        'purchase_id': 'count',  # Frequency
        'purchase_amount': 'sum'  # Monetary
    }).reset_index()
    
    # Rename columns
    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    
    # Create scoring quartiles (4 is best, 1 is worst)
    rfm['R'] = pd.qcut(rfm['recency'], q=4, labels=[4, 3, 2, 1])  # Reversed for recency
    rfm['F'] = pd.qcut(rfm['frequency'], q=4, labels=[1, 2, 3, 4])
    rfm['M'] = pd.qcut(rfm['monetary'], q=4, labels=[1, 2, 3, 4])
    
    # Calculate RFM Score (weighted)
    rfm['rfm_score'] = (
        rfm['R'].astype(int) * 0.35 +  # Recency weight
        rfm['F'].astype(int) * 0.35 +  # Frequency weight
        rfm['M'].astype(int) * 0.30    # Monetary weight
    ).round(2)
    
    # Create customer segments based on RFM score
    def segment_customer(score):
        if score >= 3.5:
            return 'Champions'
        elif score >= 3.0:
            return 'Loyal Customers'
        elif score >= 2.5:
            return 'Potential Loyalists'
        elif score >= 2.0:
            return 'At Risk'
        else:
            return 'Lost Customers'
    
    rfm['customer_segment'] = rfm['rfm_score'].apply(segment_customer)
    
    # Add segment description
    segment_descriptions = {
        'Champions': 'Bought recently, buy often, and spend the most',
        'Loyal Customers': 'Regular customers with above average spend',
        'Potential Loyalists': 'Recent customers with average frequency',
        'At Risk': 'Past customers with below average recency',
        'Lost Customers': 'Lowest scores in all categories'
    }
    
    rfm['segment_description'] = rfm['customer_segment'].map(segment_descriptions)
    
    # Calculate additional metrics
    rfm['days_since_last_purchase'] = rfm['recency']
    rfm['average_purchase_value'] = rfm['monetary'] / rfm['frequency']
    
    # Round numeric columns
    rfm['average_purchase_value'] = rfm['average_purchase_value'].round(2)
    
    return rfm

# Generate sample datasets
customer_df = generate_customer_data(1000)
campaign_df = generate_campaign_data(50)
engagement_df = generate_engagement_data(customer_df['customer_id'].tolist(), 5000)
purchase_df = generate_purchase_data(customer_df['customer_id'].tolist(), 3000)
referral_df = generate_referral_data(customer_df['customer_id'].tolist(), 1000)
loyalty_df = generate_loyalty_data(customer_df['customer_id'].tolist())

# Calculate RFM scores
rfm_df = calculate_rfm_scores(purchase_df)

# Save to CSV files
customer_df.to_csv('sample_customer_data.csv', index=False)
campaign_df.to_csv('sample_campaign_data.csv', index=False)
engagement_df.to_csv('sample_engagement_data.csv', index=False)
purchase_df.to_csv('sample_purchase_data.csv', index=False)
referral_df.to_csv('sample_referral_data.csv', index=False)
loyalty_df.to_csv('sample_loyalty_data.csv', index=False)
rfm_df.to_csv('sample_rfm_data.csv', index=False)

# Print sample of each new dataset
print("\nSample Purchase Data:")
print(purchase_df.head())
print("\nSample Referral Data:")
print(referral_df.head())
print("\nSample Loyalty Data:")
print(loyalty_df.head())

# Print RFM analysis summary
print("\nRFM Analysis Summary:")
print("\nCustomer Segments Distribution:")
print(rfm_df['customer_segment'].value_counts())
print("\nRFM Score Statistics:")
print(rfm_df['rfm_score'].describe())
print("\nSample RFM Data:")
print(rfm_df.head())



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
    # Calculate derived metrics
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

# Generate sample datasets
customer_df = generate_customer_data(1000)
campaign_df = generate_campaign_data(50)
engagement_df = generate_engagement_data(customer_df['customer_id'].tolist(), 5000)

# Example of saving to CSV
customer_df.to_csv('sample_customer_data.csv', index=False)
campaign_df.to_csv('sample_campaign_data.csv', index=False)
engagement_df.to_csv('sample_engagement_data.csv', index=False)

# Print sample of each dataset
print("\nSample Customer Data:")
print(customer_df.head())
print("\nSample Campaign Data:")
print(campaign_df.head())
print("\nSample Engagement Data:")
print(engagement_df.head())

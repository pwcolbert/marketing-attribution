import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

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

# Generate all the previous datasets
customer_df = generate_customer_data(1000)
campaign_df = generate_campaign_data(50)
engagement_df = generate_engagement_data(customer_df['customer_id'].tolist(), 5000)
purchase_df = generate_purchase_data(customer_df['customer_id'].tolist(), 3000)
referral_df = generate_referral_data(customer_df['customer_id'].tolist(), 1000)
loyalty_df = generate_loyalty_data(customer_df['customer_id'].tolist())

# Calculate RFM scores
rfm_df = calculate_rfm_scores(purchase_df)

# Save all datasets to CSV files
customer_df.to_csv('sample_customer_data.csv', index=False)
campaign_df.to_csv('sample_campaign_data.csv', index=False)
engagement_df.to_csv('sample_engagement_data.csv', index=False)
purchase_df.to_csv('sample_purchase_data.csv', index=False)
referral_df.to_csv('sample_referral_data.csv', index=False)
loyalty_df.to_csv('sample_loyalty_data.csv', index=False)
rfm_df.to_csv('sample_rfm_data.csv', index=False)

# Print RFM analysis summary
print("\nRFM Analysis Summary:")
print("\nCustomer Segments Distribution:")
print(rfm_df['customer_segment'].value_counts())
print("\nRFM Score Statistics:")
print(rfm_df['rfm_score'].describe())
print("\nSample RFM Data:")
print(rfm_df.head())

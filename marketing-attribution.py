import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import beta
import warnings
warnings.filterwarnings('ignore')

class MarketingAttribution:
    def __init__(self, touchpoints_df, conversions_df):
        """
        Initialize with touchpoint and conversion data
        
        Parameters:
        touchpoints_df: DataFrame with columns [customer_id, timestamp, channel, interaction_type]
        conversions_df: DataFrame with columns [customer_id, timestamp, conversion_value]
        """
        self.touchpoints = touchpoints_df.copy()
        self.conversions = conversions_df.copy()
        self.touchpoints['timestamp'] = pd.to_datetime(self.touchpoints['timestamp'])
        self.conversions['timestamp'] = pd.to_datetime(self.conversions['timestamp'])

    def last_click_attribution(self):
        """A. Last-click attribution: Assigns 100% credit to the last touchpoint"""
        results = []
        
        for _, conversion in self.conversions.iterrows():
            # Get touchpoints before conversion
            customer_touches = self.touchpoints[
                (self.touchpoints['customer_id'] == conversion['customer_id']) &
                (self.touchpoints['timestamp'] <= conversion['timestamp'])
            ]
            
            if not customer_touches.empty:
                last_touch = customer_touches.sort_values('timestamp').iloc[-1]
                results.append({
                    'channel': last_touch['channel'],
                    'value': conversion['conversion_value']
                })
        
        return pd.DataFrame(results).groupby('channel')['value'].sum().reset_index()

    def first_click_attribution(self):
        """B. First-click attribution: Assigns 100% credit to the first touchpoint"""
        results = []
        
        for _, conversion in self.conversions.iterrows():
            customer_touches = self.touchpoints[
                (self.touchpoints['customer_id'] == conversion['customer_id']) &
                (self.touchpoints['timestamp'] <= conversion['timestamp'])
            ]
            
            if not customer_touches.empty:
                first_touch = customer_touches.sort_values('timestamp').iloc[0]
                results.append({
                    'channel': first_touch['channel'],
                    'value': conversion['conversion_value']
                })
        
        return pd.DataFrame(results).groupby('channel')['value'].sum().reset_index()

    def linear_attribution(self):
        """C. Linear attribution: Distributes credit equally across all touchpoints"""
        results = []
        
        for _, conversion in self.conversions.iterrows():
            customer_touches = self.touchpoints[
                (self.touchpoints['customer_id'] == conversion['customer_id']) &
                (self.touchpoints['timestamp'] <= conversion['timestamp'])
            ]
            
            if not customer_touches.empty:
                value_per_touch = conversion['conversion_value'] / len(customer_touches)
                for _, touch in customer_touches.iterrows():
                    results.append({
                        'channel': touch['channel'],
                        'value': value_per_touch
                    })
        
        return pd.DataFrame(results).groupby('channel')['value'].sum().reset_index()

    def time_decay_attribution(self, half_life=7):
        """D. Time-decay attribution: Assigns more credit to touchpoints closer to conversion"""
        results = []
        
        for _, conversion in self.conversions.iterrows():
            customer_touches = self.touchpoints[
                (self.touchpoints['customer_id'] == conversion['customer_id']) &
                (self.touchpoints['timestamp'] <= conversion['timestamp'])
            ]
            
            if not customer_touches.empty:
                # Calculate time weights
                time_diffs = (conversion['timestamp'] - customer_touches['timestamp']).dt.total_seconds() / (24 * 3600)
                weights = np.exp(-np.log(2) * time_diffs / half_life)
                total_weight = weights.sum()
                
                # Distribute value based on weights
                for weight, (_, touch) in zip(weights, customer_touches.iterrows()):
                    results.append({
                        'channel': touch['channel'],
                        'value': conversion['conversion_value'] * (weight / total_weight)
                    })
        
        return pd.DataFrame(results).groupby('channel')['value'].sum().reset_index()

    def multi_touch_attribution(self, position_weights={'first': 0.3, 'middle': 0.2, 'last': 0.5}):
        """E. Multi-touch attribution: Assigns different weights based on position"""
        results = []
        
        for _, conversion in self.conversions.iterrows():
            customer_touches = self.touchpoints[
                (self.touchpoints['customer_id'] == conversion['customer_id']) &
                (self.touchpoints['timestamp'] <= conversion['timestamp'])
            ].sort_values('timestamp')
            
            if not customer_touches.empty:
                n_touches = len(customer_touches)
                
                for idx, (_, touch) in enumerate(customer_touches.iterrows()):
                    if n_touches == 1:
                        weight = 1
                    elif idx == 0:
                        weight = position_weights['first']
                    elif idx == n_touches - 1:
                        weight = position_weights['last']
                    else:
                        weight = position_weights['middle'] / (n_touches - 2) if n_touches > 2 else position_weights['middle']
                    
                    results.append({
                        'channel': touch['channel'],
                        'value': conversion['conversion_value'] * weight
                    })
        
        return pd.DataFrame(results).groupby('channel')['value'].sum().reset_index()

    def algorithmic_attribution(self):
        """F. Algorithmic attribution: Uses machine learning to determine channel importance"""
        # Prepare features for each conversion
        features = []
        values = []
        
        for _, conversion in self.conversions.iterrows():
            customer_touches = self.touchpoints[
                (self.touchpoints['customer_id'] == conversion['customer_id']) &
                (self.touchpoints['timestamp'] <= conversion['timestamp'])
            ]
            
            if not customer_touches.empty:
                # Create channel presence features
                channel_counts = customer_touches['channel'].value_counts()
                channel_features = pd.Series(0, index=self.touchpoints['channel'].unique())
                channel_features[channel_counts.index] = channel_counts
                
                features.append(channel_features)
                values.append(conversion['conversion_value'])
        
        if features:
            # Train Random Forest model
            X = pd.DataFrame(features)
            y = values
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            # Calculate channel importance
            importance = pd.DataFrame({
                'channel': X.columns,
                'value': model.feature_importances_ * sum(values)
            })
            return importance.sort_values('value', ascending=False)
        
        return pd.DataFrame(columns=['channel', 'value'])

    def probabilistic_attribution(self, n_iterations=1000):
        """G. Probabilistic modeling: Uses Bayesian approach to estimate channel contribution"""
        channel_conversions = {}
        channel_non_conversions = {}
        
        # Count conversions and non-conversions for each channel
        for channel in self.touchpoints['channel'].unique():
            channel_customers = self.touchpoints[self.touchpoints['channel'] == channel]['customer_id'].unique()
            converting_customers = self.conversions['customer_id'].unique()
            
            conversions = len(set(channel_customers) & set(converting_customers))
            non_conversions = len(set(channel_customers) - set(converting_customers))
            
            channel_conversions[channel] = conversions
            channel_non_conversions[channel] = non_conversions
        
        results = []
        # Use Beta distribution to model conversion probability
        for channel in channel_conversions.keys():
            alpha = channel_conversions[channel] + 1
            beta_param = channel_non_conversions[channel] + 1
            
            # Sample from Beta distribution
            samples = beta.rvs(alpha, beta_param, size=n_iterations)
            
            # Calculate expected value and confidence interval
            results.append({
                'channel': channel,
                'value': np.mean(samples) * self.conversions['conversion_value'].sum(),
                'confidence_95': np.percentile(samples, [2.5, 97.5])
            })
        
        return pd.DataFrame(results)

    def incremental_attribution(self, control_group_data):
        """H. Incremental attribution: Measures lift compared to control group"""
        results = []
        
        for channel in self.touchpoints['channel'].unique():
            # Get conversion rates for treatment and control groups
            channel_customers = self.touchpoints[self.touchpoints['channel'] == channel]['customer_id'].unique()
            
            treatment_conversions = len(set(channel_customers) & set(self.conversions['customer_id']))
            treatment_rate = treatment_conversions / len(channel_customers) if len(channel_customers) > 0 else 0
            
            control_conversions = len(set(control_group_data['customer_id']) & set(self.conversions['customer_id']))
            control_rate = control_conversions / len(control_group_data['customer_id']) if len(control_group_data) > 0 else 0
            
            # Calculate incremental lift
            incremental_lift = treatment_rate - control_rate
            incremental_value = incremental_lift * len(channel_customers) * self.conversions['conversion_value'].mean()
            
            results.append({
                'channel': channel,
                'incremental_lift': incremental_lift,
                'value': incremental_value
            })
        
        return pd.DataFrame(results)

# Example usage
def generate_sample_data(n_customers=1000, n_touchpoints=5000, n_conversions=500):
    """Generate sample data for testing attribution models"""
    channels = ['Paid Search', 'Social Media', 'Email', 'Display', 'Organic Search']
    
    # Generate touchpoints
    touchpoints = []
    for _ in range(n_touchpoints):
        customer_id = random.randint(1, n_customers)
        timestamp = datetime.now() - timedelta(days=random.randint(0, 90))
        channel = random.choice(channels)
        interaction_type = random.choice(['click', 'view', 'engage'])
        
        touchpoints.append({
            'customer_id': customer_id,
            'timestamp': timestamp,
            'channel': channel,
            'interaction_type': interaction_type
        })
    
    # Generate conversions
    conversions = []
    converted_customers = random.sample(range(1, n_customers + 1), n_conversions)
    for customer_id in converted_customers:
        timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
        conversion_value = random.uniform(50, 500)
        
        conversions.append({
            'customer_id': customer_id,
            'timestamp': timestamp,
            'conversion_value': conversion_value
        })
    
    # Generate control group data
    control_group = pd.DataFrame({
        'customer_id': range(n_customers + 1, n_customers + 201),
        'group': 'control'
    })
    
    return (
        pd.DataFrame(touchpoints),
        pd.DataFrame(conversions),
        control_group
    )

# Generate sample data
touchpoints_df, conversions_df, control_group_df = generate_sample_data()

# Initialize attribution model
attribution = MarketingAttribution(touchpoints_df, conversions_df)

# Run all attribution models and save results
results = {
    'last_click': attribution.last_click_attribution(),
    'first_click': attribution.first_click_attribution(),
    'linear': attribution.linear_attribution(),
    'time_decay': attribution.time_decay_attribution(),
    'multi_touch': attribution.multi_touch_attribution(),
    'algorithmic': attribution.algorithmic_attribution(),
    'probabilistic': attribution.probabilistic_attribution(),
    'incremental': attribution.incremental_attribution(control_group_df)
}

# Save results to CSV files
for model_name, result_df in results.items():
    result_df.to_csv(f'attribution_{model_name}.csv', index=False)

# Print summary of results
print("\nMarketing Attribution Analysis Summary:")
for model_name, result_df in results.items():
    print(f"\n{model_name.replace('_', ' ').title()} Attribution Results:")
    print(result_df)

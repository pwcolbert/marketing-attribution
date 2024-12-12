# marketing-attribution

Over the last 4 months I've been extending one of my research projects and working with a client on omnichannel recency-frequency-monetary analysis (RFM) + marketing attribution (ecommerce traffic sources include browser-based, app-based, social, email). 

I've implemented similar features in several client environments earlier in my career on Oracle (PL-SQL) and Microsoft SQL Server (T-SQL) databases. 

Since I'm using open source Python libraries this time, I thought I would share my proof-of-concept starting point on Github (https://github.com/pwcolbert/marketing-attribution) for my colleagues working on similar efforts. It's been a rewarding project involving a good bit of integration with existing systems beyond the sample data that you generate in the 'marketing-data-generator' file. 

In the end, I find it to be a straightforward but powerful way to put marketing theory into practice --> developing customer insights from journey, interaction, referral, and transaction data in an accessible way. Hope you get some value out of it!

I created a set of starter scripts that generate six types of omnichannel marketing data. To use them, you'll need pandas and numpy installed. 

1. Customer Data:
   - Demographics (age groups, locations)
   - Acquisition sources
   - Signup dates

2. Campaign Data:
   - Campaign details and types
   - Performance metrics (impressions, clicks, conversions)
   - Calculated KPIs (CTR, conversion rate, CPC, CPA)

3. Engagement Data:
   - Customer interactions and events
   - Event timestamps
   - Associated values

4. Purchase Data:
   - Tracks individual purchases with product categories
   - Includes payment methods
   - Records purchase amounts and quantities
   - Tracks discounts applied

5. Referral Data:
   - Records customer referral activities
   - Tracks referral channels and status
   - Includes referral bonuses
   - Links referred customers when conversions happen

6. Loyalty Data:
   - Manages customer loyalty tiers and points
   - Tracks points earned and redeemed
   - Includes tier benefits
   - Records reward redemption history

The script saves the data to CSV files and also prints a sample of each dataset. You can modify the parameters (like num_records) to generate more or less data as needed.

Each dataset is interconnected through customer_id, allowing you to perform complex analyses across different aspects of customer behavior. The data is realistic and includes:
- Natural distributions of values
- Logical relationships between fields
- Appropriate null values where relevant
- Consistent date ranges

//////////////////
//////////////////

The Recency-Frequency-Monetary RFM analysis function performs some useful scoring capabilities.

1. Calculates base RFM metrics:
   - Recency: Days since last purchase
   - Frequency: Number of purchases
   - Monetary: Total spending

2. Assigns scores (1-4) for each RFM component using quartiles

3. Calculates a weighted RFM score with:
   - 35% weight for Recency
   - 35% weight for Frequency
   - 30% weight for Monetary

4. Segments customers into five categories:
   - Champions (score ≥ 3.5)
   - Loyal Customers (score ≥ 3.0)
   - Potential Loyalists (score ≥ 2.5)
   - At Risk (score ≥ 2.0)
   - Lost Customers (score < 2.0)

5. Includes additional metrics:
   - Days since last purchase
   - Average purchase value
   - Segment descriptions

The results are saved in 'sample_rfm_data.csv' alongside the other datasets. The function also prints a summary of the customer segment distribution and RFM score statistics.

//////////////////
//////////////////

The MarketingAttribution class implements eight different attribution models:

1. Last-click Attribution:
   - Assigns all credit to the final touchpoint before conversion
   - Best for immediate response campaigns

2. First-click Attribution:
   - Credits the initial touchpoint
   - Useful for understanding acquisition channels

3. Linear Attribution:
   - Distributes credit equally across all touchpoints
   - Provides balanced view of the customer journey

4. Time-decay Attribution:
   - Weights touchpoints based on proximity to conversion
   - Customizable half-life parameter

5. Multi-touch Attribution:
   - Assigns different weights based on position
   - Configurable weights for first, middle, and last touches

6. Algorithmic Attribution:
   - Uses Random Forest to determine channel importance
   - Data-driven approach based on patterns

7. Probabilistic Attribution:
   - Bayesian approach with Beta distribution
   - Includes confidence intervals

8. Incremental Attribution:
   - Compares against control group
   - Measures true lift from each channel

The code includes:
- Sample data generation
- Comprehensive documentation
- Results saved to separate CSV files
- Summary statistics for each model

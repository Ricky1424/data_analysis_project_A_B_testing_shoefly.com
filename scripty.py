import pandas as pd

# Load the ad clicks data from CSV file
ad_clicks = pd.read_csv('ad_clicks.csv')

# Part one - print the first 5 rows
# print(ad_clicks.head(5))

# Part two - Show where is the highest UTM source.
# Group by 'utm_source' and count the number of user_ids for each source
utm_source_clicks = ad_clicks.groupby('utm_source').user_id.count().reset_index()
# Rename id column as count
utm_source_clicks = utm_source_clicks.rename(columns={'user_id': 'count'})
# Order by the highest first and drop the extra index column
utm_source_clicks = utm_source_clicks.sort_values(by='count', ascending=False).reset_index(drop=True)
# print(utm_source_clicks)

# Part three - Create 'is_click' column based on 'ad_click_timestamp' column
ad_clicks['is_click'] = ad_clicks['ad_click_timestamp'].notnull()
# print(ad_clicks)

# Part four - Group by 'utm_source' and 'is_click', count user_ids
clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()
# print(clicks_by_source)

# Part five - Pivot the 'clicks_by_source' DataFrame to calculate percentage of clicks
clicks_by_source_pivot = clicks_by_source.pivot(
  columns='is_click',
  index='utm_source',
  values='user_id'
).reset_index()

# Part six - Calculate percentage of clicks and add a new column to the pivot table
clicks_by_source_pivot['percent_clicked'] = round((clicks_by_source_pivot[True] / (clicks_by_source_pivot[True] + clicks_by_source_pivot[False])) * 100, 2)
print(clicks_by_source_pivot)

# Part seven - Group by 'experimental_group' and 'is_click', count user_ids
ad_visibility = ad_clicks.groupby(['experimental_group', 'is_click']).user_id.count().reset_index()

# Pivot the 'ad_visibility' DataFrame to calculate percentage of clicks
ad_visibility_pivot = ad_visibility.pivot(
  columns='is_click',
  index='experimental_group',
  values='user_id'
).reset_index()

# Part eight - Calculate percentage of clicks and add a new column to the pivot table
ad_visibility_pivot['percent_clicked'] = round((ad_visibility_pivot[True] / (ad_visibility_pivot[True] + ad_visibility_pivot[False])) * 100, 2)
print(ad_visibility_pivot)

# Part nine - Separate data for experimental groups A and B
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

# Part ten - Group by day and 'is_click', count user_ids, and calculate percentage of clicks for group A
a_clicks = a_clicks.groupby([a_clicks.day, a_clicks.is_click]).user_id.count().reset_index()
a_clicks_pivot = a_clicks.pivot(
  columns='is_click',
  index='day',
  values='user_id'
)
a_clicks_pivot['percent_clicked'] = round((a_clicks_pivot[True] / (a_clicks_pivot[True] + a_clicks_pivot[False])) * 100, 2)
print(a_clicks_pivot)

# Part ten: B - Group by day and 'is_click', count user_ids, and calculate percentage of clicks for group B
b_clicks = b_clicks.groupby([b_clicks.day, b_clicks.is_click]).user_id.count().reset_index()
b_clicks_pivot = b_clicks.pivot(
  columns='is_click',
  index='day',
  values='user_id'
)
b_clicks_pivot['percent_clicked'] = round((b_clicks_pivot[True] / (b_clicks_pivot[True] + b_clicks_pivot[False])) * 100, 2)
print(b_clicks_pivot)
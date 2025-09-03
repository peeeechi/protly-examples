import pandas as pd
import plotly.express as px
import os

# Create a sample CSV data
csv_data = """id,value1,value2,category
1,10,25,A
2,15,30,B
3,8,20,A
4,22,45,C
5,18,35,B
"""

# Save the data to a temporary CSV file
with open('temp_data.csv', 'w') as f:
    f.write(csv_data)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('temp_data.csv')

# Create a bar chart
fig_bar = px.bar(df, x='id', y='value1', color='category', title='Value1 by Category')

# Create a scatter plot
fig_scatter = px.scatter(df, x='value1', y='value2', color='category', title='Value1 vs Value2')

# Create output directory if it doesn't exist
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the plots as separate HTML files in the output directory
fig_bar.write_html(os.path.join(output_dir, 'bar_chart.html'))
fig_scatter.write_html(os.path.join(output_dir, 'scatter_plot.html'))

print('Successfully generated bar_chart.html and scatter_plot.html')
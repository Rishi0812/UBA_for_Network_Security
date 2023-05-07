import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

# Set up the initial pie chart
data = pd.read_csv('flows.csv')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
value_counts = data['src_ip'].value_counts()
percentages = 100 * value_counts / len(data)
patches, texts, autotexts = ax1.pie(percentages, labels=percentages.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('bright'), textprops={'fontsize': 12})
ax1.axis('equal')
ax1.set_title('Source IP Distribution', fontsize=14, fontweight='bold')

# Set up the initial histogram
sns.histplot(data=data, x='timestamp', y='pkt_size_avg', bins=20, cmap='coolwarm', edgecolor='white', alpha=0.8, color='darkorange', ax=ax2)
ax2.set_title('Packet Size Distribution', fontsize=14, fontweight='bold')
ax2.set_xlabel('Timestamp', fontsize=12)
ax2.set_ylabel('Packet Size (bytes)', fontsize=12)

while True:
    # Read the latest data
    data = pd.read_csv('flows.csv')

    # Update the pie chart
    value_counts = data['src_ip'].value_counts()
    percentages = 100 * value_counts / len(data)
    for i, autotext in enumerate(autotexts):
        autotext.set_text('{:.1f}%'.format(percentages[i]))
    ax1.set_title('Source IP Distribution (Updated)', fontsize=14, fontweight='bold')

    # Update the histogram
    ax2.clear()
    sns.histplot(data=data, x='timestamp', y='pkt_size_avg', bins=20, cmap='coolwarm', edgecolor='white', alpha=0.8, color='darkorange', ax=ax2)
    ax2.set_title('Packet Size Distribution (Updated)', fontsize=14, fontweight='bold')

    # Wait for 5 minutes before updating the charts again
    time.sleep(300)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


file_path = 'CleanHistoricalDataSP500.csv'
data = pd.read_csv(file_path)

# Date column to datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y')
data.sort_values(by='Date', inplace=True)
data.set_index('Date', inplace=True)

#Daily Returns
data['Daily Return'] = data['Close/Last'].pct_change() * 100  

#Monthly Returns
data['Month'] = data.index.to_period('M')
monthly_returns = data.groupby('Month')['Close/Last'].apply(lambda x: (x.iloc[-1] / x.iloc[0] - 1) * 100)  

#Annual Returns
data['Year'] = data.index.to_period('Y')
annual_returns = data.groupby('Year')['Close/Last'].apply(lambda x: (x.iloc[-1] / x.iloc[0] - 1) * 100) 

#Annual Growth Rate
total_years = (data.index[-1] - data.index[0]).days / 365.25
cagr = ((data['Close/Last'].iloc[-1] / data['Close/Last'].iloc[0]) ** (1 / total_years) - 1) * 100  

#Maximum Drawdowns
running_max = data['Close/Last'].cummax()
drawdowns = (data['Close/Last'] / running_max - 1) * 100
max_drawdown = drawdowns.min()

#Maximum Loss in a Year
max_loss_year = data.groupby('Year')['Close/Last'].apply(lambda x: (x / x.cummax() - 1).min() * 100)  

# Analytics Summary
analytics = {
    "Average Annual Returns": annual_returns.mean(),
    "Annual Growth Rate (CAGR)": cagr,
    "Maximum Drawdown": max_drawdown,
    "Average Maximum Loss by Year": max_loss_year.mean(),
}

#Visualizations
plt.figure(figsize=(14, 7))

#Cumulative Returns Line Chart
plt.subplot(2, 2, 1)
cumulative_returns = (1 + data['Daily Return'] / 100).cumprod()  
plt.plot(data.index, cumulative_returns, label='Cumulative Returns')
plt.title('Cumulative Returns')
plt.xlabel('Date')
plt.ylabel('Growth of $1')
plt.legend()

#Annual Returns Bar Chart
plt.subplot(2, 2, 2)
annual_returns.plot(kind='bar', color='skyblue')
plt.title('Annual Returns')
plt.xlabel('Year')
plt.ylabel('Return (%)')
plt.xticks(rotation=0)

#Monthly Returns Bar Chart
plt.subplot(2, 2, 3)
monthly_returns.plot(kind='bar', color='orange')
plt.title('Monthly Returns')
plt.xlabel('Month')
plt.ylabel('Return (%)')
plt.xticks(ticks=range(0, len(monthly_returns), 6), labels=monthly_returns.index[::6].strftime('%Y-%m'), rotation=45)
#Drawdowns Line Chart
plt.subplot(2, 2, 4)
plt.plot(drawdowns, color='red')
plt.title('Drawdowns Over Time')
plt.xlabel('Date')
plt.ylabel('Drawdown (%)')

plt.tight_layout()
plt.savefig('financial_analysis_charts.png')

# SAnalytics converted to text
with open('analytics_summary.txt', 'w') as f:
    for key, value in analytics.items():
        f.write(f"{key}: {value:.2f}%\n")

# New Data
processed_file_path = 'Processed_HistoricalDataSP500.csv'
data.to_csv(processed_file_path)


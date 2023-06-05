import csv
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            date = datetime.strptime(row[0], '%Y-%m-%d')
            value = float(row[1])
            data.append((date, value))
    return data

# Read first CSV file
file1_path = 'MORTGAGE30US.csv'
mortgage_rates = pd.read_csv(file1_path)
mortgage_rates['DATE'] = pd.to_datetime(mortgage_rates['DATE'])
mortgage_rates.set_index('DATE', inplace=True)

# Read second CSV file
file2_path = 'MSPUS.csv'
home_prices = pd.read_csv(file2_path)
home_prices['DATE'] = pd.to_datetime(home_prices['DATE'])
home_prices.set_index('DATE', inplace=True)


def calculate_monthly_cost(home_price, interest_rate, loan_term=30):
    # Convert interest rate to monthly interest rate
    monthly_interest_rate = interest_rate / 100 / 12

    # Convert loan term to months
    loan_term_months = loan_term * 12

    # Calculate the loan amount
    loan_amount = home_price

    # Calculate the monthly payment
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -loan_term_months)

    return monthly_payment

monthly_cost = []

for date, home_price in home_prices.iterrows():
    home_price = home_price['MSPUS']
    closest_date = min(mortgage_rates.index, key=lambda hdate: abs(hdate - date))
    mortgage_rate = mortgage_rates.loc[closest_date]['MORTGAGE30US']
    mortgage_mo = calculate_monthly_cost(home_price, mortgage_rate)
    monthly_cost.append(mortgage_mo)


# Set the plot style to a dark background
plt.style.use('dark_background')

# Set the text color to white
plt.rcParams['text.color'] = 'white'

# Set the desired figure width and height
fig_width = 14
fig_height = 7

fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))

# Plot the data on the primary axis
ax1.plot(home_prices.index.tolist(), monthly_cost, color='blue', linewidth=2.5)
ax1.set_xlabel('Date', fontsize=16)
ax1.set_ylabel('Monthly Payment', color='blue', fontsize=16)

# Create the 2nd axis
ax2 = ax1.twinx()

# Plot the data on the secondary axis
ax2.plot(home_prices.index.tolist(), home_prices['MSPUS'].tolist(), color='red', linewidth=1.5)
ax2.set_ylabel('Average Home Price', color='red', fontsize=16)

# Create the 3rd axis
ax3 = ax1.twinx()

# Plot the data on the secondary axis
ax3.plot(mortgage_rates.index.tolist(), mortgage_rates['MORTGAGE30US'].tolist(), color='green', linewidth=0.5)
ax3.set_ylabel('Interest Rate', color='green', fontsize=16, labelpad=-40)
ax3.tick_params(axis='y', pad=-20)

plt.title('Average Mortgage Over Time', fontsize=20)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend()

# Save and Display the graph
plt.savefig(f'avg_mortgage.png', dpi=float(600))
plt.show()

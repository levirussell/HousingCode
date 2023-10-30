import csv
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from datetime import timedelta

SHOW_OUTPUT = False

# Read first CSV file
# https://fred.stlouisfed.org/series/MORTGAGE30US
mortgage_rates_link = r'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=MORTGAGE30US&scale=left'
mortgage_rates = pd.read_csv(mortgage_rates_link)
mortgage_rates['DATE'] = pd.to_datetime(mortgage_rates['DATE'])
mortgage_rates.set_index('DATE', inplace=True)

# Read second CSV file
# https://fred.stlouisfed.org/series/MSPUS
home_prices_link = r'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=MSPUS&scale=left'
home_prices = pd.read_csv(home_prices_link)
home_prices['DATE'] = pd.to_datetime(home_prices['DATE'])
home_prices.set_index('DATE', inplace=True)

# Read second CSV file
# https://fred.stlouisfed.org/series/MEHOINUSA672N
median_household_income_link = r'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=MEHOINUSA672N&scale=left'
median_household_income = pd.read_csv(median_household_income_link)
median_household_income['DATE'] = pd.to_datetime(median_household_income['DATE'])
median_household_income.set_index('DATE', inplace=True)



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


date_list = []
monthly_cost = []
monthly_cost_precentage_dates = []
monthly_cost_precentage = []

for date, mortgage_rate in mortgage_rates.iterrows():

    mortgage_rate = mortgage_rate['MORTGAGE30US']

    closest_home_price_date = min(home_prices.index, key=lambda hdate: abs(hdate - date))
    home_price = home_prices.loc[closest_home_price_date]['MSPUS']

    mortgage_mo = calculate_monthly_cost(home_price, mortgage_rate)

    # Only use data if dates are close
    if date - median_household_income.index[0] > timedelta(0):
        closest_salary_date = min(median_household_income.index, key=lambda hdate: abs(hdate - date))
        closest_salary = median_household_income.loc[closest_salary_date]['MEHOINUSA672N']
        monthly_cost_precentage_dates.append(date)
        monthly_cost_precentage.append((mortgage_mo * 12)/closest_salary)

    date_list.append(date)
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
ax1.plot(date_list, monthly_cost, color='yellow', linewidth=1.0)
ax1.set_xlabel('Date', fontsize=16)
ax1.set_ylabel('Monthly Payment', color='yellow', fontsize=16)

# Create the 2nd axis
ax2 = ax1.twinx()

# Plot the data on the secondary axis
ax2.plot(home_prices.index.tolist(), home_prices['MSPUS'].tolist(), color='red', linewidth=1.0)
ax2.set_ylabel('Average Home Price', color='red', fontsize=16)

# Create the 3rd axis
ax3 = ax1.twinx()

# Plot the data on the secondary axis
ax3.plot(mortgage_rates.index.tolist(), mortgage_rates['MORTGAGE30US'].tolist(), color='green', linewidth=0.5)
ax3.set_ylabel('Interest Rate', color='green', fontsize=16, labelpad=-40)
ax3.tick_params(axis='y', pad=-20)


plt.title('Average Mortgage sub Insurance+Taxes', fontsize=20)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend()

# Save and Display the graph
plt.savefig(f'avg_mortgage.png', dpi=float(600))
if SHOW_OUTPUT:
    plt.show()


# Output 2nd graph

fig2, ax_1 = plt.subplots(figsize=(fig_width, fig_height))

# Plot the data on the secondary axis
ax_1.plot(median_household_income.index.tolist(), median_household_income['MEHOINUSA672N'].tolist(), color='green', linewidth=1.0)
ax_1.set_xlabel('Date', fontsize=16)
ax_1.set_ylabel('Household Income', color='green', fontsize=16)


# Create the 2nd axis
ax_2 = ax_1.twinx()

# Plot the data on the secondary axis
ax_2.plot(monthly_cost_precentage_dates, monthly_cost_precentage, color='yellow', linewidth=1.0)
ax_2.set_ylabel('Yearly Mortgage Payment as Percent of Income', color='yellow', fontsize=16, labelpad=20)


plt.title('Average Yearly Mortgage as Percent of Household Income', fontsize=20)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend()

# Save and Display the graph
plt.savefig(f'mortgage_to_income.png', dpi=float(600))
if SHOW_OUTPUT:
    plt.show()

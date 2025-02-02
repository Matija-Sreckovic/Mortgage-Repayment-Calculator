import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Mortgage Repayment Calculator")

st.write("### Input Data")
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value", min_value=0, value=500000)
deposit = col1.number_input("Deposit", min_value=0, value=100000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=5.5)
loan_term = col2.number_input("Loan Term (in years)", min_value = 1, value=30)

#Calculate the repayments.
loan_amount = home_value - deposit
monthly_interest_rate = interest_rate / 1200
number_of_payments = loan_term*12
monthly_payment = monthly_interest_rate*loan_amount*((1+monthly_interest_rate)**number_of_payments)/((1+monthly_interest_rate)**number_of_payments - 1)

#Display the repayments
total_payment = monthly_payment*number_of_payments
total_interest = total_payment - loan_amount

st.write("### Repayment")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly payment", value=f"${monthly_payment:.2f}")
col2.metric(label="Total payment (excluding deposit)", value=f"${total_payment:.2f}")
col3.metric(label="Total interest (excluding deposit)", value=f"${total_interest:.2f}")

#Create a DataFrame with payment schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    remaining_balance *= (1+monthly_interest_rate)
    remaining_balance -= monthly_payment
    year = math.ceil(i/12) #Calculate the year into the loan
    schedule.append([i, remaining_balance, year])

df = pd.DataFrame(schedule, columns = ["Month", "Remaining Balance", "Year"])

#Display df as a chart
st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)



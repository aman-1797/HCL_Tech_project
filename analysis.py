# Online Customer Behaviour Analysis
# Simple beginner project using pandas and tabulate

import pandas as pd
from tabulate import tabulate

# Load the data
df = pd.read_csv("Online customer behaviour analysis.csv")

print("========== Online customer behaviour analysis ==========")

# 1. Total orders and total completed-order value and sales
total_orders = len(df)
completed = df[df["Status"] == "Completed"]
total_completed_value = completed["Order_Value"].sum()
total_sales = df["Order_Value"].sum()

table1 = [
    ["Total Orders", total_orders],
    ["Total Completed-Order Value", total_completed_value],
    ["Total Sales (All Orders)", total_sales]
]
print("\n1. Total Orders and Sales")
print(tabulate(table1, headers=["Metric", "Value"], tablefmt="grid"))

# 2. Categories and cities contributing most to orders and sales
category_sales = df.groupby("Category")["Order_Value"].sum().sort_values(ascending=False)
city_sales = df.groupby("City")["Order_Value"].sum().sort_values(ascending=False)

table2 = [
    ["Top Category", category_sales.index[0], category_sales.iloc[0]],
    ["Top City", city_sales.index[0], city_sales.iloc[0]]
]
print("\n2. Top Category and City by Sales")
print(tabulate(table2, headers=["Type", "Name", "Sales"], tablefmt="grid"))

# 3. Proportion of customers placing more than one order
orders_per_customer = df.groupby("Customer_ID")["Order_ID"].count()
repeat_customers = (orders_per_customer > 1).sum()
total_customers = len(orders_per_customer)
repeat_percent = (repeat_customers / total_customers) * 100

table3 = [
    ["Repeat Customers (>1 order)", repeat_customers],
    ["Total Customers", total_customers],
    ["Proportion (%)", round(repeat_percent, 2)]
]
print("\n3. Customers Placing More Than One Order")
print(tabulate(table3, headers=["Metric", "Value"], tablefmt="grid"))

# 4. Average order value difference between customer groups
df["Group"] = df["Customer_ID"].map(
    lambda x: "Repeat" if orders_per_customer[x] > 1 else "One-time"
)
group_avg = df.groupby("Group")["Order_Value"].mean().round(2)

table4 = [[group, avg] for group, avg in group_avg.items()]
print("\n4. Average Order Value by Customer Group")
print(tabulate(table4, headers=["Customer Group", "Average Order Value"], tablefmt="grid"))

# 5. Rates of cancellation and return
cancelled = (df["Status"] == "Cancelled").sum()
returned = (df["Status"] == "Returned").sum()
cancel_rate = (cancelled / total_orders) * 100
return_rate = (returned / total_orders) * 100

table5 = [
    ["Cancellation Rate (%)", round(cancel_rate, 2)],
    ["Return Rate (%)", round(return_rate, 2)]
]
print("\n5. Cancellation and Return Rates")
print(tabulate(table5, headers=["Metric", "Value"], tablefmt="grid"))

# 6. Longer delivery durations and lower customer ratings
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Delivery_Date"] = pd.to_datetime(df["Delivery_Date"])
df["Delivery_Days"] = (df["Delivery_Date"] - df["Order_Date"]).dt.days

delivery_rating = df.groupby("Rating")["Delivery_Days"].mean().round(2)
correlation = round(df["Delivery_Days"].corr(df["Rating"]), 2)

table6 = [[rating, days] for rating, days in delivery_rating.items()]
print("\n6. Delivery Days vs Customer Rating")
print(tabulate(table6, headers=["Customer Rating", "Average Delivery Days"], tablefmt="grid"))
print("Correlation between delivery days and rating:", correlation)

# 7. Customer segments showing stronger repeat-purchase behaviour
segment = df.groupby("Group").agg(
    total_orders=("Order_ID", "count"),
    total_customers=("Customer_ID", "nunique")
)
segment["orders_per_customer"] = (segment["total_orders"] / segment["total_customers"]).round(2)

print("\n7. Customer Segments and Repeat-Purchase Behaviour")
print(tabulate(segment, headers="keys", tablefmt="grid"))

# 8. Actions to improve customer experience
recommendations = [
    "Reduce delivery delays to improve ratings",
    "Improve packaging to reduce returns and cancellations",
    "Offer discounts to one-time customers to encourage repeat orders",
    "Focus marketing on top categories and cities",
    "Collect feedback from cancelled and returned orders"
]

table8 = [[i+1, rec] for i, rec in enumerate(recommendations)]
print("\n8. Recommended Actions to Improve Customer Experience")
print(tabulate(table8, headers=["#", "Action"], tablefmt="grid"))

print("\n========== ANALYSIS COMPLETE ==========")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import env
import acquire

def get_store_item_sales_clean():
    if os.path.exists("./store_item_sales.csv"):
        # read in the data
        store_items = pd.read_csv("store_item_sales.csv", index_col= 0)
    else:
        db_name = "tsa_item_demand"
        query = """
        SELECT *
        FROM items
        JOIN sales USING(item_id)
        JOIN stores USING(store_id);
        """

        # using codeup dataset
        store_items = pd.read_sql(query, env.get_db_access(db_name))

        # save to csv
        store_items.to_csv("./store_item_sales.csv", mode= "w")
        
    # change the datatype of sale date
    store_items.sale_date = store_items.sale_date.astype("datetime64")
    
    # set index
    store_items = store_items.set_index("sale_date")
    
    # Add a 'month' and 'day of week' column to your dataframe
    store_items["month"] = store_items.index.month
    store_items["month_name"] = store_items.index.month_name()
    store_items["weekday"] = store_items.index.weekday
    store_items["weekday_name"] = store_items.index.day_name()
    store_items["day"] = store_items.index.day
    
    # create a total sale colum
    store_items["sales_total"] = store_items.sale_amount * store_items.item_price

    return store_items

def get_ops_clean():
    ops = pd.read_csv("https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv")

    # covert date columns to datetime
    ops.Date = ops.Date.astype("datetime64")
    
    # Set index
    ops = ops.set_index("Date")
    
    cols = ops.columns
    for i in cols:
        ops[i] = ops[i].fillna(ops[i].mean())
    
    ops["year"] = ops.index.year
    ops["month"] = ops.index.month
    ops["month_name"] = ops.index.month_name()
    
    return ops
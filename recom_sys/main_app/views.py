from django.shortcuts import render
from django.http import HttpResponse
import os
import pandas as pd
import random
from .rec_sys import product_rec_cuid_pid



file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(file_path)
cust_info_path = os.path.join(file_dir, 'static', 'cust_info.csv')
product_info_path = os.path.join(file_dir, 'static', 'prod_info.csv')
image_path =  os.path.join(file_dir, 'static', 'cart.png')
image_path_big =  os.path.join(file_dir, 'static', 'big_cart.jpg')
print(image_path)
def recommendation_view(request):
    customer_data = pd.read_csv(cust_info_path)
    product_info = pd.read_csv(product_info_path)
    if request.method == 'POST':
        # Get the selected customer_unique_id and product_id from the form submission
        customer_unique_id = request.POST.get('customer_id')
        product_id = request.POST.get('product_id')
        location = customer_data[customer_data['customer_unique_id'] == customer_unique_id]['customer_state'].iloc[0]
        print(location)
        print(customer_unique_id)
        print(product_id)
        # Call the recommendation function with the selected customer_unique_id and product_id
        recommendations = product_rec_cuid_pid(customer_unique_id, product_id)

        # Pass the recommendations to the template for display
        return render(request, 'recommendation_result.html', {'recommendations': recommendations, 'customer_id': customer_unique_id, 'product_id': product_id, 'image_path' :image_path_big, 'customer_state': location})
    else:
        # Load customer data from CSV file
        # customer_data = pd.read_csv(cust_info_path)
        customer_ids = random.sample(customer_data['customer_unique_id'].tolist(),20)
        # product_info = pd.read_csv(product_info_path)
        product_data = product_info[['product_id', 'product_category', 'price', 'avg_total_review']].values.tolist()
        product_ids = random.sample(product_data, 20)
        product_ids = [[item[0], item[1].title().replace('_', ' '), round(item[2],2), round(item[3],1)] for item in product_ids]
        # product_ids = random.sample(product_info['product_id'].tolist(),20)
        return render(request, 'prod_select.html', {'customer_ids': customer_ids, 'product_ids': product_ids, 'image_path' :image_path})

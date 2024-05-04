import os
import pandas as pd


file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(file_path)
cust_info_path = os.path.join(file_dir, 'static', 'cust_info.csv')
product_info_path = os.path.join(file_dir, 'static', 'prod_info.csv')

product_info = pd.read_csv(product_info_path)
cust_info = pd.read_csv(cust_info_path)


def product_rec_cuid_pid(customer_unique_id, product_id):

  recom_dict = {}

  #similar_products
#   print('similar products:')
  prod_record = product_info[product_info['product_id'] == product_id].iloc[0]
  prod_cat = prod_record['product_category']
  prod_price = prod_record['price']
  prod_rating = prod_record['avg_total_review']
  prod_in_cat = product_info[product_info['product_category'] == prod_cat]
  # print(prod_in_cat)
  prod_in_cat = prod_in_cat[['product_id','product_category', 'price', 'avg_total_review']]
  prod_in_cat_sorted = prod_in_cat.sort_values(by='avg_total_review', ascending=False, inplace = True)
  # print(prod_in_cat)
  similar_prods = prod_in_cat.head(10).values.tolist()
  similar_prods = [[item[0], item[1].title().replace('_', ' '), round(item[2],2), round(item[3],1)] for item in similar_prods]
  recom_dict['curr_cat'] = prod_cat.title().replace('_', ' ')
  recom_dict['curr_price'] = round(prod_price,2)
  recom_dict['curr_review'] = round(prod_rating, 1)
  recom_dict['sim_prod'] = similar_prods







  # based on previous purchases
#   print('\n\nbased on previous purchases:')
  prev_pids = cust_info[cust_info['customer_unique_id'] == customer_unique_id]['product_ids'].iloc[0]
  prev_pids = list(prev_pids.split(','))
#   print('previous purchases:',prev_pids)
  prev_categories = []

  # Extract categories of previous purchases
  for pid in prev_pids:
      prod_cat = product_info[product_info['product_id'] == pid]['product_category'].iloc[0]
      prev_categories.append(prod_cat)
  
#   print('categories:',prev_categories)

  # Get all products in categories of previous purchases
  products_in_categories = product_info[product_info['product_category'].isin(prev_categories)][['product_id','product_category', 'price', 'avg_total_review']]

  # Sort products by average review in descending order
  sorted_products = products_in_categories.sort_values(by='avg_total_review', ascending=False)

  # Get top 10 products
  previous_purchases =  sorted_products.head(10).values.tolist()
  previous_purchases = [[item[0], item[1].title().replace('_', ' '), round(item[2],2), round(item[3],1)] for item in previous_purchases]
  recom_dict['prev_purch'] = previous_purchases



  #based on similiar clusters
#   print('\n\nbased on similiar clusters')
  cust_cluster = cust_info[cust_info['customer_unique_id'] == customer_unique_id]['Cluster_Label'].iloc[0]
#   print('Customer cluster:',cust_cluster)
  filter_bycluster = cust_info[cust_info['Cluster_Label'] == cust_cluster]
  split_ids = filter_bycluster['product_ids'].str.split(',')
  all_ids = [id for sublist in split_ids for id in sublist]
  unique_ids = list(set(all_ids))
  # print(unique_ids)
  filtered_product_info = product_info[product_info['product_id'].isin(unique_ids)][['product_id','product_category', 'price', 'avg_total_review']]
  sorted_products = filtered_product_info.sort_values(by='avg_total_review', ascending=False)
#   print(top_ten_products_clust)
  cluster_recomm = sorted_products.head(10).values.tolist()
#   print('cluster_recomm:', cluster_recomm)
  cluster_recomm = [[item[0], item[1].title().replace('_', ' '), round(item[2],2), round(item[3],1)] for item in cluster_recomm]
  recom_dict['cluster_recomm'] = cluster_recomm


  #based on location
#   print('\n\nbased on location:')
  cust_loc = cust_info[cust_info['customer_unique_id'] == customer_unique_id]['customer_state'].iloc[0]
#   print('Customer State:', cust_loc)
  filter_byloc = cust_info[cust_info['customer_state'] == cust_loc]
  split_ids = filter_byloc['product_ids'].str.split(',')
  all_ids = [id for sublist in split_ids for id in sublist]
  unique_ids = list(set(all_ids))
  filtered_product_info = product_info[product_info['product_id'].isin(unique_ids)][['product_id','product_category', 'price', 'avg_total_review']]
  sorted_products = filtered_product_info.sort_values(by='avg_total_review', ascending=False)
#   print(top_ten_products_loc)
  loc_recomm = sorted_products.head(10).values.tolist()
  loc_recomm = [[item[0], item[1].title().replace('_', ' '), round(item[2],2), round(item[3],1)] for item in loc_recomm]
#   print('loc_recomm:', loc_recomm)
  recom_dict['loc_recomm'] = loc_recomm
#   print(recom_dict)

  return recom_dict



    




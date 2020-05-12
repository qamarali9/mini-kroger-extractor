"""
This script makes calls to kroger api for getting product details.
CLIENT_ID and CLIENT_SECRET are obtained via registration.
The execution starts via start().
product_ids is the list of product ids of the products whose details are being fetched.
Initially an OAuth access token is required for making calls to the API, which is fetched by get_oauth2_access_token.
Then each individual product details are fetched by making API calls.
"""

import requests
import base64
import json

def get_oauth2_access_token(CLIENT_ID,CLIENT_SECRET):
    """
    Gets the access token required for making subsequent API calls for fetching product details
    The equivalent curl request :
    curl -X POST \
            'https://api.kroger.com/v1/connect/oauth2/token' \
            -H 'Content-Type: application/x-www-form-urlencoded' \
            -H 'Authorization: Basic {{base64(“CLIENT_ID:CLIENT_SECRET”)}}' \
            -d 'grant_type=client_credentials&scope={{SCOPE}}'
    """
    
    # Base64 encoded CLIENT_ID:CLIENT_SECRET required in the header for getting the access token
    creds_base64 = base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, "utf-8")).decode("utf-8")
    #print(creds_base64)
    #"ZmV0Y2hwcm9kdWN0aW5mby1hOTM4NGRmYWZiYWM2MzZiN2FjY2U0ZWY5ZWRlMTliMjMwMjMyODY4MDA1MTg1NzE5NzY6a1RDRFJUZGRiM0p3RWZ1Y2tKTHB0VjU0S0RJcThQdmpPdXdaOEx4MQ=="

    access_token_url = "https://api.kroger.com/v1/connect/oauth2/token"
    headers = {
            "Content-Type" : "application/x-www-form-urlencoded",
            "Authorization" : "Basic " + creds_base64,
            }
    payload = {
            "grant_type": "client_credentials",
            "scope": "product.compact",
            }
    # Make the post request with appropriate headers and pay-load, and get the response
    response = requests.post(access_token_url,headers=headers,data=payload)
    #print(response.status_code)
    if(response.status_code == requests.codes.ok):
        #print(response.headers,response.headers["Content-Type"],response.text)
        response_text_dict = json.loads(response.text)
        #print(response_text_dict)
        access_token = response_text_dict.get("access_token","") # Get access token from the response json
        if(access_token != ""):
            return access_token
        
    print("ERROR:Could not get access token")
    return None


def get_product_details(product_id,access_token):
    """
    Gets the product detail json for the product with product_id using access_token
    The equivalent curl request :
    curl -X GET \
            'https://api.kroger.com/v1/products/{{ID}}' \
            -H 'Accept: application/json' \
            -H 'Authorization: Bearer {{TOKEN}}'
    """
    product_url = "https://api.kroger.com/v1/products/" +  product_id
    headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + access_token,
    }
    response = requests.get(product_url,headers=headers)
    #print(response.status_code)
    if(response.status_code == requests.codes.ok):
        return json.loads(response.text) # Return the product details as python dictionary

    print("ERROR:Could not get product detail for product_id:"+product_id)
    return None


def start():
    CLIENT_ID = "fetchproductinfo-a9384dfafbac636b7acce4ef9ede19b23023286800518571976"
    CLIENT_SECRET = "kTCDRTddb3JwEfuckJLptV54KDIq8PvjOuwZ8Lx1"
    
    product_ids = ["0000000004011", "0003338320027", "0003450015136", "0001111040101", "0001111041700", "0004460032064", "0000000004046"]
    
    access_token = get_oauth2_access_token(CLIENT_ID,CLIENT_SECRET)
    
    if(access_token == None):
        return
    
    for product_id in product_ids:
        product_details = get_product_details(product_id,access_token)
        if(product_details != None):
            print(product_details)

if __name__ == "__main__":
    start()

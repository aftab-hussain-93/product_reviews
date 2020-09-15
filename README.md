# PRODUCT REVIEW
### Follow the below steps for initialization:

    pip install -r requirements.txt

##### Database sample data :   
Data from a sample e-commerce dataset available in /sample-data. 300 random products are chosen and inserted into the database. These products are then inserted with a random number of reviews, along with a rating score. The rating score number is between 1-5.

Run file database_initialize.py using below command to initalize the database items.
  
```
python3 database_initialize.py
```

##### Run the flask app. 

  ```
  py run.py 
  ```    
    Go to http://localhost:5000/ for the application front end.

##### API Endpoints available to manipulate and view the data.  

```
GET -
http://localhost:5000/api/product_rating    
Response - [{  
  "product_name" : ..,  
  "public_key":..,  
  "rating_score":..,  
  "reviews": all_the reviews  
  }, { prod n details...}]  
```

```
GET -
http://localhost:5000/api/product_rating/<product_public_key>   
Response - For a single product  
{  
  "product_name" : ..,  
  "public_key":..,  
  "rating_score":..,  
  "reviews": all_the reviews  
  }  
```

```    
   Endpoint to add a review for a Product  
   POST-  
   http://localhost:5000/api/add_review  

    Expected Input:  
  {  
		"product_id" : <UUID/PublicKey of Product>,  
		"rating" : <Rating (1-5)>,  
		"review_string" : <Review string>  
	}  
  Expected Response:    
	Response 400  
	{  
		"error": <error message>  
	}  
	Response 200:  
	{  
		"message": <review added to DB>:<new rating string NOT evaluated>,  
		"product_id" : <UUID/PublicKey of Product>,  
		"review_evaluated" : "True if new reviews were evaluated, False if not>  
	}  
	Response 201:    
	{  
		"message": <review added to DB and new rating string IS evaluated>,  
		"product_id" : <UUID/PublicKey of Product>,  
		"review_evaluated" : "True if new reviews were evaluated, False if not>  
	}  
```

```

Endpoint to get public keys for all products  
GET-  
http://localhost:5000/api/all_products
[
  {
  "name": product name, 
  "public_key": product key
  }
]
```

```
Endpoint to get details for particular product  
GET-  
http://localhost:5000/api/product/<public_key>
Expected Response - 
  {
      'product_name': <name>, 
      'public_key': <public_key>, 
      'rating_string' : <rating string> , 
      'reviews_ratings': [ 
          { 
          'rating' : < 1-5 > ,
          'review_count' : <count of reviews with this rating>
          }
       ]                        
  }
```

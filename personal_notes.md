### DELIVERABLES/REQUIREMENTS

1. Deploy the model as an endpoint on a RESTful service which receives JSON
 POST data.
 The inputs to this endpoint should be the columns in
 data/future_unseen_examples.csv .
 The endpoint should return a JSON object
 with a prediction from the model, as well as any metadata you see as
 necessary.
 The inputs to the endpoint should not include any of the demographic
 data from the 
data/zipcode_demographics.csv table.  Your service should
 add this data on the backend.
 Consider how your solution would scale as more users call the API.
 If possible, design a solution that allows scaling up or scaling down of API
 resources without stopping the service.  You don't have to actually
 implement autoscaling, but be prepared to talk about how you would.
 Consider how updated versions of the model will be deployed.
 If possible, develop a solution that allows new versions of the model to be
 deployed without stopping the service.
 Bonus: the basic model only uses a subset of the columns provided in the
 house sales data.
 Create an additional API endpoint where only the required features have
 to be provided in order to get a prediction.
 2. Create a test script which submits examples to the endpoint to demonstrate
 its behavior.  The examples should be taken from
 data/future_unseen_examples.csv .
 This script does not have to be complicated, only needs to demonstrate
 that the service works.
3. Evaluate the performance of the model.  You should start with the code
 in 
create_model.py and try to figure out how well the model will generalize
 to new data.  Has the model appropriately fit the dataset

 ## ------ ##

 Questions:

 1- What are the real expected features? It says in instructions that is the columns from data/future_unseen_examples.csv, and we have "model_features.json" file that has slightly different amount of columns.
 
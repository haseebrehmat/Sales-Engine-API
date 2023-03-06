from ssm_parameter_store import SSMParameterStore
store = SSMParameterStore(prefix='/CloudBuild')
# access a parameter under /Prod/ApiSecret
my_secret = store['AKIAQDQXUW4VYD2VFME3']
# check if a parameter available in the store
if 'MyKey' in store:
    # list available parameters
    print(store.keys())
    # access parameter under Db prefix
    db_store = store['Db']
    # this will query /Prod/Db/Password
    my_db_password = db_store['Password']
    # or you can also do
    my_db_password = store['Db']['Password']


# import boto3
#
# AWS_REGION = "us-west-1"
# ssm_client = boto3.client("ssm", region_name=AWS_REGION)
# # creating paginator object for describe_parameters() method
# paginator = ssm_client.get_paginator('describe_parameters')
# # creating a PageIterator from the paginator
# page_iterator = paginator.paginate().build_full_result()
# # loop through each page from page_iterator
# for page in page_iterator['Parameters']:
#     response = ssm_client.get_parameter(
#         Name=page['Name'],
#         WithDecryption=True
#     )
#
#     value = response['Parameter']['Value']
#
#     print("Parameter Name is: " + page['Name'] + " and Value is: " + value)
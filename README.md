# Lap 4 project

# Welcome to PreLoved! 

## Description
Have you ever wanted to get new clothes but don't know what to do with the old ones? Then this is the perfect place for you. Preloved is a website that allows you to search for clothes that you want to get new and get them for free.

# Local Setup instructions

1. run `pipenv install` in the terminal to install all the dependencies
2. run `pipenv install --dev` to install dev dependancies (if you want to examine the testing results and coverage)
3. run `pipenv shell` to enter the virtual environment
4. run `pipenv run dev` to run the development server
5. run `pipenv run test` to run the tests
6. run `pipenv run coverage` to run the coverage report


<hr>

# API useage
Here are the routes for using the API along with their expected receiving and sending data

## <ins>Main routes</ins>

## Index/root url - `/` - optional paramaters `user`, `category`
- Allowed methods:  
    - GET: Retrieves all from clothing items data, allowing for filtering via optional paramaters allowing you to retrieve entries from a single `user` or by `category` returning an array of JSON data. 
    <br> Exected response example: <br> 
    ```JSON
    [{
        "category": "t-shirt",
        "description": "cool t-shirt",
        "id": 1, // id of item
        "images": "url_to_item_images", // url to firebase servers
        "item_name": "item 1",
        "on_offer": false,
        "size": "M",
        "user_id": "1a2b3c" // id of user who created item
    },]
    ```

## <ins>Auth routes</ins>

## Create new list item - `/new-listing`
- Allowed methods: 
    - POST: Creates new `clothing_item` table entry from JSON request. 
    <br> Exected request example: <br> 
    ```JSON
    {
        "item_name": "clothing item",
        "item_desc": "descriptive text",
        "item_cat": "dress",
        "item_size": "M",
        "item_user_id": "1a2b3c", // id of user who created item
        "item_images": "url_to_item_images" // url to firebase servers
    }
    ```

## Register - `/auth/register`
- Allowed methods:  
    - POST: Creates new `user` table entry from JSON request expecting the following keys: <br>
     ```JSON
    {
        "username": "username",
        "password": "password",
        "email": "email@mail.com",
        "location": "city"
    }
     ```

## Login - `/auth/login`
- Allowed methods:  
    - POST: Searches through database for valid `user` to login and return `JWT`. 
    <br> Request is expected to contain the following keys within a basic auth: <br> 
    `'username', 'password'`, no JSON body is required


## Message another user - `/auth/msg`
Current user is determined by the `user_id` decoded within the `JWT`, which when sent along side the request is used to create and access messages.

- Allowed methods:  
    - GET: Retrieve all messages sent by or too `user_id` from `JWT` and returns them in JSON.  
    Exected JSON response example: <br> 
    ```JSON
    {"Messages": [
		{
            "message_id": 1,
            "message_date" : "datetime",
			"message_text": "Hello world",
			"sender": "4e5f6h", // user id - sender of message
			"receiver": "1a2b3c", // user id - recipient of message
            "sender_name": "sender_username",
            "receiver_name": "receiver_username"
		}
    ]}
    ```
    - POST: Create new entry within the `message` table.
    <br> Expect message in JSON format with the following keys: <br> 
    ```JSON
    {
        "message_text": "Hello world",
        "user_id": "1a2b3c", // user id - sender of message
        "receiver_id": "4e5f6h" // user id - recipient of message
    }
    ```

## Propose offer - `/auth/create-swap`
Current user/proposer of offer is determined by the `user_id` decoded within the `JWT`, which when sent along side the request.

- Allowed methods:  
    - POST: Create new entry within the `offer` table.
    <br> Exected JSON request example: <br> 
    ```JSON
    {
        "proposer_item_id": 4, //clothing item id
        "reciever": "a1b2c3", //user id of proposal reciever
        "reciever_item_id": 5, //clothing item id
    }
    ```

## Update offer - `/auth/update-swap-status`
Update existing `offer` status's with `pending`, `accepted`, `rejected` along with other relevent tables data.

- Allowed methods:  
    - PUT: Update existing entry within the `offer` table.
    <br> Exected JSON request example: <br> 
    ```JSON
    {
        "offer_id": 4, 
        "proposer_item_id": 2, //clothing item id
        "status": "accepted",  // new status to update existing
    }
    ```

## Return all offers - `/auth/offers`  - optional paramaters `user`
Optional paramater of `user` allows for narrowing down offers by '`proposer`'
- Allowed methods:  
    - GET: Searches through database for all `offer` entries and returns them in JSON.  
    Exected response example: <br> 

    ```JSON
    {[
        {
            "id": 1,
            "proposer": "a1b2c3",
            "proposer_item_id": 2,
            "reciever": "d4f4g6",
            "reciever_item_id": 3,
            "offer_status": "pending"
        },
    ]}
    ```

## Return all users - `/auth/users`
`TESTING PURPOSES` do not use in production
- Allowed methods:  
    - GET: Searches through database for all `user` entries and returns them in JSON.  
    Exected response example: <br> 

    ```JSON
    {"users": [
        {
            "email": "test@test.com",
            "id": "1a2b3c",
            "location": "New York",
            "password": "test",
            "username": "michael"
        },
    ]}
    ```
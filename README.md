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

## Index/root url - `/`
- Allowed methods:  
    - GET: Retrieves all from clothing items data, allowing for filtering via optional paramaters returning an array of JSON data. 
    <br> Exected response example: <br> 
    ```JSON
    [{
        "category": "t-shirt",
        "description": "cool t-shirt",
        "id": 1, // id of item
        "images": "url_to_item_images",
        "item_name": "item 1",
        "on_offer": false,
        "size": "M",
        "user_id": "1a2b3c" // id of user who created item
    },]
    ```

## Create new list item - `/new-listing`
- Allowed methods: 
    - POST: Creates new `clothing_item` database entry from Form request. 
    <br>Expects the following valid fields:  <br> 
    `'item_name', 'item_desc', 'item_cat', 'item_size', 'item_user_id', 'item_images'`

## <ins>Auth routes</ins>

## Register - `/auth/register`
- Allowed methods:  
    - POST: Creates new `user` database entry from JSON request expecting the following keys: <br> 
    `'username', 'password', 'email', 'location'`

## Login - `/auth/login`
- Allowed methods:  
    - POST: Searches through database for valid `user` to login and return `JWT`. 
    <br> Request is expected to contain the following keys within a basic auth: <br> 
    `'username', 'password'`, no JSON or body is required


## Return all users - `/auth/users`
`TESTING PURPOSES` do not use in production
- Allowed methods:  
    - GET: Searches through database for all `user` entries and returns them in JSON.  <br> Exected response example: <br> 

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

## Message another user - `/auth/msg/<string:user_id>`
Url contains paramater of `user_id` that is used to both send and retrieve messages, is sent to local storage along with `JWT`.

- Allowed methods:  
    - GET: Retrieve all messages sent by or too `user` and returns them in JSON.  
    Exected JSON response example: <br> 
    ```JSON
    {"Messages": [
		{
            "message_id": 1,
            "message_date" : "datetime",
			"message_text": "Hello world",
			"receiver": "1a2b3c", // user id - recipient of message
			"sender": "4e5f6h" // user id - sender of message
		},
    ]}
    ```
    - POST: Create new entry within the `message` database.
    <br> Expect message in JSON format with the following keys: <br> 
    ```JSON
    {
        "message_text": "Hello world",
        "user_id": "1a2b3c", // user id - sender of message
        "receiver_id": "4e5f6h" // user id - recipient of message
    }
    ```
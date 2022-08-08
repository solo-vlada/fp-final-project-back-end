# Lap 4 project

# Welcome to PreLoved! 

## Description
Have you ever wanted to get new clothes but don't know what to do with the old ones? Then this is the perfect place for you. Preloved is a website that allows you to search for clothes that you want to get new and get them for free.

## Local Setup instructions

1. run `pipenv install` in the terminal to install all the dependencies
2. run `pipenv install --dev` to install dev dependancies (if you want to examine the testing results and coverage)
3. run `pipenv shell` to enter the virtual environment
4. run `pipenv run dev` to run the development server
5. run `pipenv run test` to run the tests
6. run `pipenv run coverage` to run the coverage report


## API useage
Here are some of the routes for using the API along with their expected received and sent data

## <ins>Main routes</ins>

### Index/root url - `/`
- Allowed methods:  
    - GET: Retrieves all from clothing items data, allowing for filtering via optional paramaters returning the data within JSON.

### Create new list item - `/new-listing`
- Allowed methods: 
    - POST: Creates new `clothing_item` database entry from Form request expecting the following valid fields:  <br> 
    `'item_name', 'item_desc', 'item_cat', 'item_size', 'item_user_id', 'item_images'`

## <ins>Auth routes</ins>

### Register - `/auth/register`
- Allowed methods:  
    - POST: Creates new `user` database entry from JSON request expecting the following keys: <br> 
    `'username', 'password', 'email', 'location'`

### Login - `/auth/login`
- Allowed methods:  
    - POST: Searches through database for valid `user` to login and return `JWT`. Request is expected to contain the following keys within a basic auth: <br> 
    `'username', 'password'`, no JSON or body is required


### See users - `/auth/users`
- Allowed methods:  
    - GET: Searches through database for all `user` entries and returns them in JSON. Exected response example: <br> 

    ```javascript
    {"users": [
        {
        "email": "test@test.com",
        "id": 1,
        "location": "New York",
        "password": "test",
        "username": "michael"
        },
    ]}
    ```

   
   
 
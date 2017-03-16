# Steam Tracker API (Google Oauth2.0 and Steam API)
    1. Get User's information  (get requiest with inline parameter) Standard URL: '/User'
       a. Handle invalid access token (checked)
       b. Handle no access token input case (checked)
       c. Handle non exist account  
    2. Post (Register User in the API) (google access token and steam id inside json varibalei) Standard URL: '/addUser'
       a. Handle invalid access token (checked)
       b. Handle repeated registered (checked)
    3. Delete (delete one user from the database and associated game)
       a. Handle invalid access token
       b. Handle no access token input case
       c. Handle non exist account  
       
 

### Heroku URL
(https://sheltered-fjord-56349.herokuapp.com)

# Project 2 - Sprint 1
This webapp aims to deliver an app that teaches people about NFTs. The app will be purposed towards users who are first getting into NFTs or haven’t even heard of them before. It will provide users with information that lets them know everything they need to know about NFTs. This includes what they are, why they are so popular and expensive, how you would purchase them, etc. The app will also show users specific NFTs and display it’s real time details and explain to them what it all means. Overall, the purpose of the app is to teach users about NFTs, including what they are as a whole, the specific details of individual NFTs, and how they can start investing in NFTs

### Technologies used in project

- __Azure virtual machine__
    We used was Azure virtual machine to store our data. We used this machine to be able 
    to run linux and code remotely.Using a device like a mac/pc to run the virtual machine 
    on Visual studio.

- __Visual studio__
    We used visual studio to code our program and to help us access our virtual machine using ssh

- __CSS and HTML__
    We used css and html for frontend. To design our webpage and make it user friendly.
    
- __Python__ 
    We used python for backend. We coded our whole program in python since it more sever freindly which
    helps us delpoy web apps easier.

- __Github__
    We used github to store our program. There we are able to store and share or files as well as a backup
    incase we lose our project.

- __Jinja2__
    We used this as a template engine for our frame work with Flask. It allowed us to render our HTML and CSS.

- __Linting__
    Used this to format your Python code with Black to make it look better.

### Frameworks used in the project 

- __Flask__
    We used flask to be able to run an application using python and display a local webpage. 
    With flask we were able to develop web applications easily.Since it provides us 
    with the tools to easily help with routing and fetching, and HTML/CSS for layout.
    We downloaed this into our machine which lets us deploy flask.


- __Heroku__
    This frameworks is used to deploy our webpage on the cloud. Which allows us to remotely 
    access our webpage. We downloed this into our machine which lets us use heroku commands. 

- __Heroku PostgreSQL__
    This is the cloud database where we upload username and artist id's to be stored

- __Flask-SQLAlchemy__
    This is a Flask extension providing an object-relational mapping (ORM) between the Postgres
    database which is Heroku and our Python logic.

- __HTML Forms__
    These are HTML elements that can be used to send HTTP POST requests to the server containing
    data that can be persisted in the DB.

- __Flask-Login__
 Flask extension for managing user sessions. Gives your server the ability to track whether the viewer is logged in, and if so, who the viewer is.



    

### Libraries 

- __Requests__
    Request is and HTTP library that allows us to send HTTP/1.1 requests easily thats also allows
    us to use the json method when dealing with API's.

- __python-dotenv__
    This lilbrary reads key-value pairs from a .env file and can set them as environment variables.
    It helps in the development of applications following the 12-factor principles.We used this to
    hide our API keys using gitignore to hide the .env file.

- __os__
    This lilbrary module in Python provides functions for interacting with the operating system.



### APIs

- __OpenSea API__
    We used this API to pull NFTs. With it we were able to pull the NFTs image,name,collection,
    collection descriptions,description of nft,creator,price, type of crypto it uses,trait types,traits 
    contract,address and token id. We used these things to implement it into our webpage.To be able to do this 
    we needed get authorization from OpenSea.




### How to Fork

- If you want to fork this web app you would have to install and get all the frameworks and libraries.
After that you would have get the OpenSea API. After that you would have to create your own .env and add your
postgresql url to match the ones in main.py. From there you your able to run the program on your machine. You can also add a gitignore file where you add your .env file to it , if you wish to push this to github so your url wont be out there in public.


### Linting
The following errors/warnings were disabled for reasons listed below:
- ```line-too-long```: Triggered only by lines containing comments that were describing the API calls. This is ignored because these it explains fuctions of the API.
- ```import-error```: For some reason it says it has an error but the app runs on heroku and local so no errors on our end.
- ```too-few-public-methods```: They were disabled because we use it as a dictionary in our database 
- ```redefined-builtin,```: We wanted to keep the fuction that name as well flet it was the best suited for that function.
- ```invalid-name```: The variable names in our files where readable or self-explanatory so we disabled it.
- ```broad-except```: Felt code ran smoothly and didn't want to affect deployment.
- ```too-many-locals```: We need alot of variables since it a big project so we disabled this.










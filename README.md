
# Blog API

Simple Blog  API built using Django and django rest framework. The website displays All blog post, specify blog and many more.
Users can create an account using **JWT Authentication**. Blog API use **Postgresql** as database

# Installation
To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with.
```bash
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```bash
virtualenv env
```

That will create a new folder env in your project directory. Next activate it with this command on mac/linux:

```bash
env\Scripts\activate
```
Then install the project dependencies with
```bash
pip install -r requirements.txt
```
Now you can run the project with this command
```bash
python manage.py runserver
```

## API Reference

#### Get all items

```http
  POST /user/create-user/
  POST /user/login/
  POST /user/refresh-token/
  POST /user/block-user/


  POST /post/post-by-user/
  GET /post/get-allpost/
  POST /post/post-archive/
  POST /post/create-post/
  POST /post/get-allpost-state/
  POST /post/get-post/
  PUT /post/update-post/19/
  DELETE /post/delete-post/
  
```



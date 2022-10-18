# Starnavi
To run project you need to install all libraries.<br/>
Enter in terminal from folder and enter:
```
$ pip install -r requirements.txt
```
Now you need to create local database. For this you need to run python as interpreter.
(For proper working you also can try to change folder to 'app')
```
$ python
```
Then enter:
```
>> from app import db
>> from app.pyfiles.models.user import User
>> from app.pyfiles.models.post import Post
>> db.create_all()
```
After this wait until file 'db.sqlite3' appears in folder 'db' in package 'app'
May be you also need (optional) to input some parameters
(secret_key). You can find it in file 'config.py' that locates in folder 'app/pyfiles'
```python
# Put here your secret key
secret = 'MY_SECRET_KEY'

```
secret - string.<br/>
After this you can run project
```
$ python run.py
```
Then there will be running server on localhost (port by default 80).<br/>
Or you can type in browser:

 * [http://127.0.0.1:80/](http://127.0.0.1:80/)

That project is web service to create new posts with possibility to like posts 
with front end and back end parts.
Created with help of Flask, JWT, Vue.js, AJAX. For database was used sqlite3
with hel of SQLalchemy. Database stores 'User' and 'Post' tables.
Object 'User' can give date of last request of user by method 'get_info()'.
Also object 'Post' stores info about likes and dates of that likes.
Basic features:

* user signup
* user login
* post creation
* post like
* post unlike
* analytics about how many likes was made. (Example url /api/analitics/?date_from=2020-02-02&date_to=2020-02-15)
* user last request (stores in db)

Project deployed on Heroku. 
 * [Link to heroku](https://starnavi-task.herokuapp.com/)
 
Thanks for feedback)

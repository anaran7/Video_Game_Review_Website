# Video_Game_Review_Website

Applications Instructions and Setup




Setup:


1. Install the database as referred by Installing_Database.pdf
2. Install the application software referred by Installing_Application_Software.pdf
3. Open settings.py file located in the following path CS480_Final_Project_Website/games_website/games_website/settings.py
   1. Find the following piece of code between lines 77 and 86
      1. DATABASES = {
      2.     'default': {
      3.         'ENGINE': 'django.db.backends.mysql',
      4.         'NAME': 'games_database',
      5.         'HOST': '127.0.0.1',
      6.         'PORT': '3306',
      7.         'USER': 'root',
      8.         'PASSWORD': '1234',
      9.     }
      10. }
      Update the host, port, user, password to correspond to your mysql database where the games_database is stored
4. Run the following commands to connect django website to your mysql database in the following path: CS480_Final_Project_Website/games_website
   1. python manage.py migrate
      1. I got the following error when trying to migrate “Authentication plugin 'caching_sha2_password' cannot be loaded” so I had to run the following command in mysql
         1. ALTER USER 'yourusername'@'localhost' IDENTIFIED WITH mysql_native_password BY 'youpassword';
      2. The migration is successful if a couple of new tables were created in your mysql database one of the being called auth_group
5. To run the website run the following command in the following path: CS480_Final_Project_Website/games_website
   1. python manage.py runserver

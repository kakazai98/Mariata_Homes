Install VS code latest version
Download and install python 3.10

Open the project foler into VS code.
 
Open a new terminal and run the following commands

pip install whitenoise
pip install django-cors-headers  
pip install django
pip install Pillow

after these are installed successfully.

Make sure your terminal is in the directory of the project where manage.py is.
Use the following command to check.

ls

Most likey you will be in the main folder so just use the following command.

cd Mariata_Homes

Run the following commands

python manage.py makemigrations website 
python manage.py sqlmigrate website 0001
python manage.py migrate
python manage.py init_sources

This will create the app for you.

Before running the server login onto mailtrap.io

look for code to connect to email service in python. You will find these 4 lines.

EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = 'a3f12cdc636e22'
EMAIL_HOST_PASSWORD = 'b2f75fb613d1e5'
EMAIL_PORT = '2525'

Your values for these variables might differ.

Copy these lines to the end of settings.py and save the file.

now run the server using :

python manage.py runserver

Open this link on any browser (preferably Chrome)

http://127.0.0.1:8000/

You have a pre-defined admin user with username: admin and password: admin
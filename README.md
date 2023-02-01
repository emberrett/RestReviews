# RestReviews

RestReviews is an open-source application for keeping track of which restaraunts you've tried, which restaurants you've liked, and other helpful information to help you plan your dining. 

You can deploy and host your clone of RestReviews on your own home server. 

## Getting Started
This guide is written with RaspberryPis running Raspbian in mind, but should be easy to tweak to fit other hardware/OS combos. 

### Things You'll Need:
* A RaspberryPi (headless is fine)
* A free Font Awesome kit code, you can get one from [here](https://fontawesome.com/start).
* A Google Maps API key, you can get one by following [this guide](https://developers.google.com/maps/documentation/javascript/get-api-key).
* A GMail account and app password, which you can get by following [this guide](https://support.google.com/accounts/answer/185833?hl=en)
* A Django secret key which you can generate by running this in Python:
```
import secrets
print(secrets.token_urlsafe())
```

<br>
<br>

>The following instructions should be performed while ssh'd into your RaspberryPi:


### Install Python
1. `sudo apt install python3 python3-venv python3-pip`

### Create the Postgres Database
1. Install postgresql with `sudo apt install postgresql`
2. Create a psql user:
```
sudo su postgres
createuser pi -P --interactive
```
>You can replace `pi` with whatever username you want. Provide your password and answer yes for granting superuser privileges when prompted.
4. Create the restreviews database:
```
psql
CREATE DATABASE restreviews;
exit
```

<br>

### Installing the Django App
1. Clone the repo. For the sake of this guide, we'll assume you've cloned into  `/home/pi/Documents/RestReviews`
2. `cd` to `/home/pi/Documents/RestReviews`
3. Create your virtual environment with `python3 -m venv djenv`
4. Activate your venv `source venv/bin/activate`
5. Install dependencies with `python3 -m pip install -r requirements.txt`

<br>

### Create and Edit .env  File
1. In the app's directory, create a .env file with `touch .env`
2. Open with `sudo nano .etv`
3. Add the following:
```
SECRET_KEY=<YOUR DJANGO SECRET KEY>
DB_NAME=restreviews
DB_USER=<YOUR_PSQL_USERNAME>
DB_PASS=<YOUR_PSQL_PASSWORD>
MAPS_API_KEY=<YOUR_MAPS_API_KEY>
FA_KEY=<YOUR_FONT_AWESOME_KIT_CODE>
DEBUG=<1_FOR_TRUE_0_FOR_FALSE>
PI_IP_ADDRESS=<YOUR_RASPBERRYPI_IP>
GMAIL_USERNAME=<YOUR_GMAIL_USERNAME>
GMAIL_PASSWORD=<YOUR_GMAIL_APP_PASSWORD>
```
4. Save and close.

<br>

### Create Database Tables and Relationships
1. In the app directory, run `python3 manage.py migrate`
>For more info on migrations in Django see [Django docs](https://docs.djangoproject.com/en/4.1/topics/migrations/).

<br>

### Install and Configure Apache Server
1. Run `sudo apt install libapache2-mod-wsgi-py3`
2. Open apache config file with `sudo nano /etc/apache2/sites-enabled/000-default.conf`
3. Add the following right before the closing `</VirtualHost>` tag:
```
Alias /static /home/pi/Documents/RestReviews/static
    <Directory /home/pi/Documents/RestReviews/static>
        Require all granted
    </Directory>

    <Directory /home/pi/Documents/RestReviews/rest-review>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess django python-path=/home/pi/documents/RestReviews python-home=/home/documents/RestReviews/venv
    WSGIProcessGroup django
    WSGIScriptAlias / /home/pi/Documents/RestReviews/rest-review/wsgi.py
```

>Note: Make sure you update with the correct file path if you've installed the app to a different location

4. Restart the Apache service with `sudo systemctl restart apache2`


### Run and Access RestReviews
* To run the Django server, run `python3 manage.py runserver runserver 0.0.0.0:8000` in the `/home/documents/RestReviews` directory.
* To automatically run the server on your RaspberryPi's startup, open `/etc/rc.local` and add these two lines before `exit 0`: 
```
source /home/pi/Documents/RestReviews/venv/bin/activate
python3 /home/pi/Documents/RestReviews/manage.py runserver 0.0.0.0:8000
```
* When the server is running, you can access RestReviews via your RaspberryPi's IP on port 8000 example: `192.168.1.4:8000`.



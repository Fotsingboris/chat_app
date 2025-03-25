Django Chat Application

This is a real-time chat application built with Django and WebSockets using Django Channels.

Features

User authentication (login/logout/register)

Real-time messaging using WebSockets

Chat rooms for group discussions

Private messaging between users

Responsive UI with Bootstrap

Installation & Setup

Follow these steps to set up the project:

1. Clone the Repository

git clone https://github.com/Fotsingboris/chat_app.git
cd django-chat-app

2. Create and Activate a Virtual Environment

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Apply Migrations

python manage.py migrate

5. Create a Superuser

python manage.py createsuperuser

6. Run the Server with Daphne

daphne chat_app.asgi:application

7. Access the Application

Open your browser and go to:

http://127.0.0.1:8000/

WebSocket Configuration

Make sure ASGI_APPLICATION is set correctly in settings.py:

ASGI_APPLICATION = 'myproject.asgi.application'

Add daphne in INSTALLED_APPS:

INSTALLED_APPS = [
    ...
    'daphne',
]

Configure CHANNEL_LAYERS (example using In-Memory backend):

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

Running with Redis (Optional for Production)

Install and run Redis:

sudo apt install redis
redis-server

Update CHANNEL_LAYERS in settings.py:

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

License

This project is licensed under the MIT License.

Author

Developed by Fotsing Tchoupe Mathieu Boris.


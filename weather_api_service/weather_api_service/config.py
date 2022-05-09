import os


app_config_dict = {
    'SQLALCHEMY_DATABASE_URI': f'sqlite:///weather_api_service.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
}

secret_key = os.environ.get('secret_key', 'FT8H9ylGnZcfhCI5SX7Q2VL46IZd1vL1')
weather_api_key = 'fd9125d0fce84c6e83d165857220605'

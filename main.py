import os
import tweepy
import spacy
from dotenv import load_dotenv

load_dotenv("variables.env")


# Credenciales de la API de Twitter
api_key = os.getenv('API_KEY')
api_secret_key = os.getenv('API_SECRET_KEY')
access_token =  os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Autenticación
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


print(api.verify_credentials().screen_name)


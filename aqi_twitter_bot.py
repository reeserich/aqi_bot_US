import numpy as np
import requests
import PIL
from PIL import Image
from datetime import datetime as dt
import tweepy

response = requests.get("https://files.airnowtech.org/airnow/today/forecast_aqi_" + 
                        dt.today().strftime("%Y%m%d") + 
                        "_usa.jpg")
file = open("temp_forecast.jpg", "wb")
file.write(response.content)
file.close()

map_img = PIL.Image.open('temp_forecast.jpg')
table_img = PIL.Image.open('aqi_chart_1.jpg')

map_img = map_img.resize((table_img.size[0], int(map_img.size[1]*table_img.size[0]/map_img.size[0])))

imgs_comb = np.vstack((map_img, table_img))
imgs_comb = PIL.Image.fromarray( imgs_comb)
imgs_comb.save('combo_image.jpg', 
               format='JPEG', 
               subsampling=0, 
               quality=100)

auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

map_tweet = api.update_with_media(filename='combo_image.jpg', 
                                  status='United States air quality forecast for ' + 
                                  dt.today().strftime("%A, %B %d, %Y") + 
                                  ':')
follow_up = api.update_status(status='For more information on this forecast and the Air Quality Index, visit AirNow.gov.', 
                              in_reply_to_status_id=map_tweet.id)
# Deep Learning Tinder (Machine Learning)
*With DIGITS, Caffe and Tinder token auto fetching*

Welcome on the Tinder Bot app whose recommandations are based on Deep Learning for image recognition. Don't forget to star or fork this repo if you appreciate the bot! 

## How does it work?

Everything is explained here: http://philipperemy.github.io/tinder-deep-learning/

## How to run the bot
```
git clone https://github.com/philipperemy/Deep-Learning-Tinder.git
cd Deep-Learning-Tinder
mv credentials.json.example credentials.json
vim credentials.json # edit and fill the variables (explained in the next section: Configuration)
python main.py
```

If the configuration file is correct, you will see in the logs: `Successfully connected to Tinder servers.`

## Configuration of credentials.json

- `FB_ID` : The id of your facebook. Your profile is available at https://www.facebook.com/FB_ID where FB_ID is your id.
- `FB_EMAIL_ADDRESS` : Your Facebook email address.
- `FB_PASSWORD` : Your Facebook password.
- `API_HOST`: URL of your NVIDIA Digits server. More information available here : https://github.com/NVIDIA/DIGITS
- `MODEL_ID`: ID of your trained model. It appears in the URL when you click on your model in the DIGITS interface, like this: `API_HOST`/models/`MODEL_ID`

`FB_EMAIL_ADDRESS` and `FB_PASSWORD` are used to retrieve your `FB_AUTH_TOKEN`, useful to request the Tinder token. 

Your configuration should look like this:

```
{
  "FB_ID": "tim.cook",
  "FB_EMAIL_ADDRESS": "tim.cook@apple.com",
  "FB_PASSWORD": "i_love_apple",
  "API_HOST": "http://localhost:5000/",
  "MODEL_ID": "20160619-000820-19f6"
}
```

Hope you will have some fun !

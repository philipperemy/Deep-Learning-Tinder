# Deep-Learning-Tinder

Welcome on the Tinder Bot whose recommandations are based on Deep Learning for image recognition. Don't forget to star or fork this repo if you appreciate the bot! 

## How to run the bot
```
git clone https://github.com/philipperemy/Deep-Learning-Tinder.git
cd Deep-Learning-Tinder
mv credentials.json.example credentials.json
vim credentials.json # edit and fill the variables (explained later)
chmod +x main.py
./main.py
```
Running `main.py` should trigger the bot `Deep Learning Tinder bot`.

A successful connection of the bot will yield `Successfully connected to Tinder servers.`

Otherwise program will exit.

## Configuration (JSON format)


`FB_ID` : the id of your facebook. Your profile is available at https://www.facebook.com/FB_ID where FB_ID is your id.

`FB_EMAIL_ADDRESS` : Your Facebook email address.

`FB_PASSWORD` : Your Facebook password.

`API_HOST` is the URL of your NVIDIA Digits server. More information is available here : https://github.com/NVIDIA/DIGITS

`MODEL_ID` is the ID of your trained model. It appears in the URL when you click on your model in the DIGITS interface, like this: `API_HOST`/models/`MODEL_ID`

`FB_EMAIL_ADDRESS` and `FB_PASSWORD` are used to retrieve your `FB_AUTH_TOKEN`, useful to request the Tinder token. Finally, you should have a configuration file that looks like this:

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

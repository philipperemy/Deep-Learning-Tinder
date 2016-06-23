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

`FB_AUTH_TOKEN` : Authentification Token of Facebook. Can be accessible here: https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token

Keep in mind that the token appears in the redirection URL and you have only a few seconds to grab it. After a few attempts, you will become better at it.

The redirection page looks like this : https://www.facebook.com/connect/login_success.html#access_token=FB_AUTH_TOKEN&expires_in=3724

where FB_AUTH_TOKEN is your own token.

### /!\ Keep in mind that the FB_AUTH_TOKEN expires usually within one or two hours. So you must re-active your bot every time.

`API_HOST` is the URL of your NVIDIA Digits server. More information is available here : https://github.com/NVIDIA/DIGITS

`MODEL_ID` is the ID of your trained model. It appears in the URL when you click on your model in the DIGITS interface, like this: `API_HOST`/models/`MODEL_ID`

Finally, you should have a configuration file that looks like this:

```
{
  "FB_ID": "philippe.remy",
  "FB_AUTH_TOKEN": "thisisawrongtoken_lBGveRJsIdvrzZCOaOZCgCoxiCb8gffoNpa5cKZA6iQPgf9PvLZBeynaCNYkZCqKEE8IwYJm0dM7EAaTTbXcpEewEdaPfFgp2iFcCNsFnEZC3ytViAfsdfdsO6h3jI4T1gZDZD",
  "API_HOST": "http://localhost:5000/",
  "MODEL_ID": "20160619-000820-19f6"
}
```

Hope you will have some fun !

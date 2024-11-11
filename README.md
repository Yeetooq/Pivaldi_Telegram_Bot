# Pivaldi Telegram Bot <img src="https://media1.tenor.com/m/ookEdv-7MlcAAAAd/barry-barry-63.gif" width="40" height="40">

<div align="center">
  <img src="https://github.com/user-attachments/assets/80ac20fa-f3d7-4feb-80ac-c1c36bd9f810" width="200" height="200">
</div>

## A brief background 📝

Initially, the project was conceived as a chat-bot for the [Pivaldi restaurant](https://pivaldi.ru/), since my groupmates and I really like to go there after couples and in our free time 🍻. Since the restaurant is actively growing and developing 📈, and the existing bot of the restaurant is frankly bad 😅, I thought I would make a good bot and contact them for further cooperation. 

The bot was made for a couple of months ⏳,and along the way I tested every little thing for an element of vulnerability. Then I tried many times to contact the managers of the restaurant , with their other departments 📞, but all attempts were in vain 😕. 

As a result, I didn't come up with anything better than just making a bot - a combined solyanka from all the interesting ideas that just come to mind 💡😄))) And how to put the project on github.


## Installation instructions 🛠️

```
# Clone the repo
git clone https://github.com/Yeetooq/Pivaldi_Telegram_Bot.git

# Enter the project folder
cd Pivaldi_Telegram_Bot

# Install dependencies
pip install -r requirements.txt
```

---

Next, in the ``` config.py ``` we change the values to our own⬇️ 

<img src="https://github.com/user-attachments/assets/f618e8cf-8548-4971-878f-0db42842b1cc" width="456" height="124">

---

* In the file handlers.py we change the ``` chat_id ``` to our own 

<img src="https://github.com/user-attachments/assets/a0b3aae9-9339-4a92-83f6-dcb93ba2b271" width="353" height="48">

---

* Insert your ``` provider_token ```

<img src="https://github.com/user-attachments/assets/c996273d-f7d2-4893-be82-c8cd732efcb0" width="344" height="116">

---

**Launching the bot 🚀**

```
python main.py
```
## Description of functions 🔧

<div align="center">
  <img src="https://github.com/user-attachments/assets/e2105e2f-59e0-426e-8646-6a51cd4d9c6f" width="428" height="640">
</div>

**Сommands:**

- ```/start``` 
  
  Launches the bot, writes the user to the database, and also issues a button with a transition to booking a place in the restaurant.

- ```/registration``` 
   
  Registers a user in the bot, can be used to access functions, but for me it's just an additional entry in the database and that's it.

- ```/catalog``` 
  
  Sends the menu of the restaurant.

- ```/pay``` 
  Allows the user to pay for their order (currently a test one).

- ```/weather```  
  
  Provides information about the current weather in the places where the restaurant is open, so that the visitor can find out about precipitation in advance and exclude unforeseen circumstances.

- ```/help```  
  
  Communication with the developer on technical issues related to the work of the bot.

- ```/help_pro```  
  
  Communication with the restaurant on service issues related to the restaurant or service.

- ```/website```  
  
  Redirects the user to the official Pivaldi website.

- ```/game``` 
  
  Starts a game where the user has to guess the number in one attempt.

- ```/statistics```  
  
  I have provided a Win Rate system in the bot to make it more interesting to play and see your luck. Shows the statistics of the user's games in the game "Guess the number from 1 time".

- ```/anekdot```  
  
  Sends a random joke to the user.

- ```/secret```
  
  My experience in the field of crypts, I just tested the codes of people from Tiktok, YouTube, etc. I also thought of interesting functions on my own.

## Database 🛢

For the project, I used the SQLite 3 database, as it is best suited for a small amount of data. The database is created automatically when the code is first run. The most convenient way to manage a database is to use SQLiteStudio.

![image](https://github.com/user-attachments/assets/1e5dabd9-9ad2-4f2b-8ebf-6aaaaf55dd96)


## + vibe✌︎︎✌︎︎

![image](https://github.com/user-attachments/assets/310d1ec0-beab-4aa8-acf0-2f1fddad8ab0)
















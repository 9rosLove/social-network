# 🌐 Social Network REST API

## 🔧 Installing using GitHub
1. Clone the repository from GitHub:
    ```bash
    git clone htthps://github.com/9rosLove/social-network.git
    cd social-network
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3. Activate a virtual enviroment:
    - For Windows🪟:
    ```bash
    .\venv\Scripts\activate
    ```
    - For Linux🐧 and MacOS🍏:
    ```bash
    source venv/bin/activate
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set the environment variables for bot configuration and secret key:
    
   - For Linux🐧 and MacOS🍏
   ```bash
    export DJANGO_SECRET_KEY=<your db hostname>
    export DJANGO_DEBUG=<True_or_False>
    ```
    - For Windows🪟
    ```shell
    set DJANGO_SECRET_KEY=<your db hostname>
    set DJANGO_DEBUG=<True_or_False>
                    ...
    ```


7. Migrate the database:
    ```bash
    python manage.py migrate
    ```
8. Start the development server:
    ```bash
    python manage.py runserver
    ```
## 🐋 Run with docker
1. Make sure Docker is installed.
2. Build the Docker containers:
    ```bash
    docker-compose build
    ```
3. Run the Docker containers:
    ```bash
    docker-compose up

# 🤖 Automated Bot
The automated bot script (bot.py) performs the following activities:

- Sign up a specified number of users.
- Each user creates a random number of posts (up to the maximum specified).
- Randomly like posts (up to the maximum specified).

## Bot Usage
### 1. Update Configuration File:
   Open the config.json file and update it according to your needs. 
   You can specify the number of users to sign up, the maximum number of posts per user, and the maximum number of likes per user.

### 2. Run Bot Script:

- Open a new terminal.
- Navigate to the bot directory:
```bash
cd bot
```
- Run the bot script using Python3:
```bash
python3 bot.py
```
### 3. If you want to use a different configuration file, you can specify it using the --config flag:
```bash
python3 bot.py --config custom_config.json
```
- The bot will use the configuration from config.json by default.

### 4. View Output:

- After running the script, you can find the output files for created users in the output directory.

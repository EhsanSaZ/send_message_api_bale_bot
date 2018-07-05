# send_message_api_bale_bot
Send_message_api_bale_bot is a simple flask app run near a bale bot in order to send text/image/file messages to a channel via http request.

Implementation was done using *Python 3.5*.

## Getting Started

### Prerequisites
    $ sudo apt-get install python3-pip python3-dev
    $ sudo pip3 install virtualenv
    $ git clone git@github.com:EhsanSaZ/send_message_api_bale_bot.git
    $ cd send_message_api_bale_bot.git
    $ sudo pip3 install -r requirements.txt
### Config
Change notification_config.py in notification/config add your own bot token. 
Set other config parameters as you prefer them.
You can change log_config in notification/config in order to use gray log for logging.
### Running the bot and server
    $ python starter.py
## Contribution
share your ideas with us about what features might improve the quality of the project.
*Feel free to contribute ! :)*
import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# This function handles the slash command and opens the modal form for the user to fill out
@app.command("/announce")
def open_announcement_modal(ack, body, client):
    # Let's slack know that you're handling the command, a requirement for every handler
    ack()
    
    try:
        # Open the modal form for the user to fill out
        client.views_open(
            trigger_id=body["trigger_id"],
            view=create_announcement_modal()
        )
        logger.info(f"Announcement modal opened by user {body['user_name']}")
    except Exception as e:
        logger.error(f"Error opening modal: {e}")

# This function handles when the user hits the `Submit` button within the modal
@app.view("announcement_modal")
def handle_announcement_submission(ack, body, view, client):
    ack()
    
    # Extract the announcement text from the modal, 
    announcement = view["state"]["values"]["announcement"]["announcement_input"]["value"]
    
    user_id = body["user"]["id"]
    user_name = body["user"]["name"]
    
    try:
        # Send announcement message
        client.chat_postMessage(
            channel=user_id, ##  Sends to your DM with the bot, but you can modify it to send to a channel of your choice instead
            text="Announcement posted! 📢",
            blocks=create_announcement_confirmation_blocks(announcement)
        )
        
        logger.info(f"Announcement posted by {user_name}: {announcement}")
        
    except Exception as e:
        logger.error(f"Error sending announcement confirmation: {e}")


# Define the modal here as functions so it's easier to read within the main functions, this is not a requirement but a stylistic choice
def create_announcement_modal():
    modal = {
        "type": "modal",
        "callback_id": "announcement_modal",
        "title": {
            "type": "plain_text",
            "text": "Team Announcement"
        },
        "submit": {
            "type": "plain_text",
            "text": "Post Announcement"
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "blocks": [
            # This is an input block that will request the announcement text from the user
            {
                "type": "input",
                # Used to identify the input block
                "block_id": "announcement",
                "element": {
                    "type": "plain_text_input",
                    # Used in conjunction with the block_id to identify this specific input block
                    "action_id": "announcement_input",
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Type your announcement here..."
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Your Announcement"
                }
            }
        ]
    }
    return modal

def create_announcement_confirmation_blocks(announcement):
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Your announcement has been posted!* 📢\n\n```{announcement}```"
            }
        }
    ]

if __name__ == "__main__":
    # Start the app
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    logger.info("🚀 Your first modal app is starting...")
    handler.start() 
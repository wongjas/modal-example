import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Slash command to open the announcement modal
@app.command("/announce")
def open_announcement_modal(ack, body, client):
    """Handle the /announce slash command and open the modal"""
    ack()
    
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=create_announcement_modal()
        )
        logger.info(f"Announcement modal opened by user {body['user_name']}")
    except Exception as e:
        logger.error(f"Error opening modal: {e}")

# Handle announcement modal submission
@app.view("announcement_modal")
def handle_announcement_submission(ack, body, view, client):
    """Handle the announcement modal submission"""
    
    # Acknowledge the modal submission
    ack()
    
    # Extract the announcement text
    values = view["state"]["values"]
    announcement = values["announcement_text"]["message_value"]["value"]
    
    user_id = body["user"]["id"]
    user_name = body["user"]["name"]
    
    try:
        # Send announcement message
        client.chat_postMessage(
            channel=user_id, ##  Uses the user ID since this requires the fewest number of steps
            text="Announcement posted! 📢",
            blocks=create_announcement_confirmation_blocks(announcement)
        )
        
        logger.info(f"Announcement posted by {user_name}: {announcement}")
        
    except Exception as e:
        logger.error(f"Error sending announcement confirmation: {e}")


# Define the modal here so it looks better within the code
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
            {
                "type": "input",
                "block_id": "announcement_text",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "message_value",
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
    """Create Block Kit message for the announcement message"""
    return [
        {
            "type": "section", 
            "text": {
                "type": "mrkdwn",
                "text": "*Your announcement has been posted!* 📢"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn", 
                "text": f"```{announcement}```"
            }
        }
    ]

if __name__ == "__main__":
    # Start the app
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    logger.info("🚀 Your first modal app is starting...")
    handler.start() 
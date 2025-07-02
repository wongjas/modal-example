TODO: This article can also be found on the slack.dev site.

# Modals

If you're learning about Slack apps, modals, or slash commands for the first time, you've come to the right place! In this tutorial, we'll take a look at setting up your very own server using Github Codespaces, and using that server to run your Slack app. Also, if you're familiar with using Heroku you can deploy directly to Heroku with the following button.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy?template=https://github.com/wongjas/modal-example)

## Let's take a look at the technologies we'll use in this tutorial: {#technologies}

* **Github Codespaces**, an online IDE that allows you to work on code and host your own server at the same time. Note Codespaces is good for testing and development purposes but should not be used in production.
* **Python** in conjunction with the [**Bolt for Python SDK**](https://github.com/SlackAPI/bolt-python).

---

## Final product overview {#final_product}
At the end of this tutorial, your final app will look like this:

TODO: Add new gif of the process

And will make use of these Slack concepts:
* [**Block Kit**](https://docs.slack.dev/block-kit/) is a UI framework for Slack apps that allows you to create beautiful, interactive messages within Slack. If you've ever seen a message in Slack with buttons or a select menu, that's Block Kit.
* [**Modals**](https://docs.slack.dev/surfaces/modals) are a pop-up window that displays right in Slack. They grab the attention of the user, and are normally used to prompt users to provide some kind of information or input in a form.
* [**Slash Commands**](https://docs.slack.dev/interactivity/implementing-slash-commands) allow you to invoke your app within Slack by just typing into the message composer box. e.g. `/remind`, `/topic` 

---

## The process {#steps}

### Setting up your app on api.slack.com
There are a couple of steps that you'll need to set up before you can start coding. This will be done on your app's settings page which you can create using the following steps:

1. [Create a new app](https://api.slack.com/apps/new) and click `From a Manifest` and choose a workspace that you want to develop on.  Next, copy the following JSON object which describes the metadata about your app like its name, its bot name and permissions that it will request.

```json
{
    "display_information": {
        "name": "Intro to Modals"
    },
    "features": {
        "bot_user": {
            "display_name": "Intro to Modals",
            "always_online": false
        },
        "slash_commands": [
            {
                "command": "/announce",
                "description": "Makes an announcement",
                "should_escape": false
            }
        ]
    },
    "oauth_config": {
        "scopes": {
            "bot": [
                "chat:write",
                "commands"
            ]
        }
    },
    "settings": {
        "interactivity": {
            "is_enabled": true
        },
        "org_deploy_enabled": false,
        "socket_mode_enabled": true,
        "token_rotation_enabled": false
    }
}
```

2. Once your app has been created, scroll down to `App-Level Tokens` and create a token that requests for the `connections:write` scope, which allows you to use [Socket Mode](https://docs.slack.dev/apis/events-api/using-socket-mode), a secure way to develop on Slack through the use of WebSockets. Copy the value of your app token and keep it for safe-keeping.

3. Install your app by heading to `Install App` in the left sidebar. Hit `Allow`, which means you're agreeing to install your app with the permissions that it is requesting and copy the token that you receive.  Also keep this in a safe spot.

### Starting your server and getting into code! {#server}

1. Make sure that you're logged into Github and head to this [repository](https://github.com/wongjas/modal-example).

2. Click the green `Code` button and hit the `Codespaces` tab and then `Create codespace on main`.  This will bring up VSCode within your browser and you can start coding.  Take a moment to see what is in the project.  Take a look at the `manifest.json` file, which is what we used to create our app and also the file `simple_modal_example.py`, which houses the code that powers your app. If you're going to tinker with the app itself, take a look at the comments found within the `simple_modal_example.py` file!

3. In the bottom panel, you should already be in the `TERMINAL` tab.  Remember the app and bot tokens that you kept safe from previous steps? We're going to use those now and set them environment variables

```bash
export SLACK_APP_TOKEN=<YOUR-APP-TOKEN-HERE>
export SLACK_BOT_TOKEN=<YOUR-BOT-TOKEN-HERE>
```

4. Activate a virtual environment for your python packages to be installed and then install the dependencies and start your app using the `python3 simple_modal_example.py` command.  You can find all those commands here:

```bash
# Setup your python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Start your local server
python3 simple_modal_example.py
```

5. Now that your app is running, you should be able to see it within Slack.  Test this by heading to Slack and typing `/announce`.

All done! 🎉 You've created your first slash command using Block Kit and modals! The world is your oyster; play around with [Block Kit Builder](https://app.slack.com/block-kit-builder) and create more complex modals and place them in your code to see what happens!

## Next steps {#next-steps}

If you want to learn more about Bolt for Python, refer to the [Getting Started guide](https://tools.slack.dev/bolt-python/getting-started).
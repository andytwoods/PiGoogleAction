import time

from flask import Flask
from flask_assistant import Assistant, tell
from pyngrok import ngrok
from pyngrok.conf import PyngrokConfig

config = {
    # "DEBUG": True,
}

app = Flask(__name__)
app.config.from_mapping(config)

app.config['INTEGRATIONS'] = ['ACTIONS_ON_GOOGLE']
assist = Assistant(app, route='/', project_id='saving-others-sanity-example')

port = 5000

# Open a ngrok tunnel to the dev server
print('setting up ngrok')

# REMEMBER: if on a Pi, create your ngrok creds file, and provide the location here
# see https://ngrok.com/docs#config
# pyngrok_config = PyngrokConfig(config_path='/home/pi/.ngrok2/ngrok.yml', region='eu')
pyngrok_config = None

# REMEMBER: replace 'gone-very-soon' with your own ngrok domain.
public_url = ngrok.connect(port, options={"subdomain": 'gone-very-soon'}, pyngrok_config=pyngrok_config)

print(f" * ngrok tunnel {public_url} -> http://127.0.0.1:{port}")

# Update any base URLs or webhooks to use the public ngrok URL
app.config["BASE_URL"] = public_url

app.config['INTEGRATIONS'] = ['ACTIONS_ON_GOOGLE']

# on a pi-zero, I found I needed a little recovery time here
time.sleep(1.0)


@assist.action('Default Welcome Intent')
def action():
    return tell("hi")


if __name__ == '__main__':
    app.run()

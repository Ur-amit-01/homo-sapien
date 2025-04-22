import os

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "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")

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Koyeb'


if __name__ == "__main__":
    app.run()

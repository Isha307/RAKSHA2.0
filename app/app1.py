from flask import Flask, render_template, Response, jsonify, request

from modules.module import modules
from auth.auth import auth

app = Flask(__name__)
app.register_blueprint(modules)
app.register_blueprint(auth)

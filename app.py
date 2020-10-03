import os

from datetime               import datetime, timedelta, date
from flask                  import Flask, jsonify, render_template
from flask_bootstrap        import Bootstrap
from flask_ponywhoosh       import PonyWhoosh
from flask_script           import Manager, Shell
from pony.orm               import *
from pony.orm.serialization import to_json

from search_network import app , socketio, db
from flask_socketio import SocketIO


if __name__ == '__main__':
   app.run(debug=True , host="0.0.0.0" , port="5000")
   
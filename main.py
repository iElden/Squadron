from flask import Flask, abort, render_template, send_from_directory
from threading import Thread
import logging
import asyncio

from DiscordClient import DiscordClient
from Global import Global
from History import GlobalHistory
from Leaders import load_leaders

logging.basicConfig(level="INFO")

load_leaders()
Global.load()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('blank.html', mapuches=Global.mapuches, didons=Global.didons)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/vendor/<path:path>')
def send_vendor(path):
    return send_from_directory('vendor', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@app.route('/squadron/<squad_query>')
def squadron_view(squad_query):
    squadron = [i for i in Global.squadrons if i.formated_name == squad_query]
    if len(squadron) != 1:
        abort(404, f"{len(squadron)} squad with this name found")
    squad = squadron[0]
    return render_template('squadron.html', mapuches=Global.mapuches, didons=Global.didons, title=squad.name, players=squad.players,
                           history=Global.full_history.get_history_for(squad), squadron=squad)

@app.route('/stats')
def stats_route():
    return render_template('blank.html', mapuches=Global.mapuches, didons=Global.didons)

@app.route('/history')
def history_route():
    return render_template('history.html', mapuches=Global.mapuches, didons=Global.didons, histories=Global.histories)

class FlaskThread(Thread):
    def run(self):
        app.run("127.0.0.1", 4000, use_reloader=False)

FlaskThread().start()
Global.loop.run_forever()
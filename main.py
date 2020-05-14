from flask import Flask, abort, render_template, send_from_directory, redirect
from threading import Thread
import logging
import asyncio

from DiscordClient import DiscordClient
from Global import Global, Constant
from History import GlobalHistory
from Leaders import load_leaders

logging.basicConfig(level="INFO")

load_leaders()
Global.load()

app = Flask(__name__)

SIDEBAR_KWARGS = {'mapuches': Global.mapuches, 'didons': Global.didons, 'christines': Global.christines}

@app.route('/')
def homepage():
    return redirect('/history')

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
    return render_template('squadron.html', **SIDEBAR_KWARGS, title=squad.name,
                           history=Global.full_history.get_history_for(squad), squadron=squad)

@app.route('/oldseason/<season_query>')
def old_season_view(season_query):
    oldseason = Global.old_season.get(season_query)
    if not oldseason:
        abort(404, f"Season \"{season_query}\" was not found")
    return render_template('oldseason.html', **SIDEBAR_KWARGS, season=season_query, data=oldseason)

@app.route('/oldseason/<season_query>/squadron/<squad_query>')
def oldsquadron_view(season_query, squad_query):
    oldseason = Global.old_season.get(season_query)
    if not oldseason:
        abort(404, f"Season \"{season_query}\" was not found")
    squadron = [i for i in oldseason.squadrons if i.formated_name == squad_query]
    if len(squadron) != 1:
        abort(404, f"{len(squadron)} squad with this name found")
    squad = squadron[0]
    return render_template('squadron.html', **SIDEBAR_KWARGS, title=f"{squad.name} (Saison {season_query})",
                           history=oldseason.get_history_for(squad), squadron=squad)

@app.route('/stats')
def stats_route():
    return render_template('blank.html', **SIDEBAR_KWARGS)

@app.route('/history')
def history_route():
    return render_template('history.html', **SIDEBAR_KWARGS, histories=Global.histories, season=Constant.CURRENT_SEASON)

class FlaskThread(Thread):
    def run(self):
        app.run("127.0.0.1", 4000, use_reloader=False)

FlaskThread().start()
Global.loop.run_forever()
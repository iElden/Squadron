from flask import Flask, abort, render_template, send_from_directory
from parse_gsheet import get_squadron

mapuches, didons = get_squadron()
squadrons = mapuches + didons

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('blank.html', mapuches=mapuches, didons=didons)

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
    squadron = [i for i in squadrons if i.formated_name == squad_query]
    if len(squadron) != 1:
        abort(404, f"{len(squadron)} squad with this name found")
    squad = squadron[0]
    return render_template('squadron.html', mapuches=mapuches, didons=didons, title=squad.name, players=squad.players)

@app.route('/stats')
def stats_route():
    return render_template('blank.html', mapuches=mapuches, didons=didons)

@app.route('/history')
def history_route():
    return render_template('blank.html', mapuches=mapuches, didons=didons)

app.run("127.0.0.1", 4000)
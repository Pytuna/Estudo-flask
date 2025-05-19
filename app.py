from flask import Flask, jsonify, abort, request, json;
from event import Event;
from eventOnline import EventOnline;

app = Flask(__name__);

ev_online = EventOnline("Curso de cozinha francesa");
ev2_online = EventOnline("Live zerando Dark Souls 2");
ev = Event("Debate acerca da constante infantilização da geração alfa na sociedade brasileira", "Praça da Bandeira");
events = [ev_online, ev2_online, ev];

@app.errorhandler(400)
def not_found(erro):
    return (jsonify(erro=str(erro)), 400);

@app.errorhandler(404)
def not_found(erro):
    return (jsonify(erro=str(erro)), 404);

@app.route("/", methods=["GET"])
def index():
    return "<h1>Flask configurado com sucesso!<h1/>";

@app.route("/eventos/", methods=["GET"])
def list_events():
    event_dict = [];
    for ev in events:
        event_dict.append(ev.__dict__);
    return jsonify(event_dict);

@app.route("/eventos/", methods=["POST"])
def make_event():
    data = json.loads(request.data);
    name = data.get("name");
    local = data.get("local");

    if not name:
        abort(400, "'nome' precisa ser informado");

    if local:
        event = Event(name=name, local=local);
    else:
        event = EventOnline(name=name);
        
    events.append(event);
    return {
        "id": event.id,
        "url": f"/eventos/{event.id}/"
    }

def get_event_or_404(id):
    for ev in events:
        if ev.id == id:
            return ev;
    abort(404, "Evento não encontrado");

@app.route("/eventos/<int:id>/")
def info_event(id):
    ev = get_event_or_404(id);
    return jsonify(ev.__dict__);

@app.route("/eventos/<int:id>/", methods=["DELETE"])
def delete_event(id):
    ev = get_event_or_404(id);
    events.remove(ev);
    return jsonify(id=id);

@app.route("/eventos/<int:id>/", methods=["PUT"])
def edit_event(id):
    data = request.get_json();
    name = data.get("name");
    local = data.get("local");

    if not name:
        abort(400, "'nome' precisa ser informado");
    if not local:
        abort(400, "'local' precisa ser informado");

    ev = get_event_or_404(id);
    ev.name = name;
    ev.local = local;

    return jsonify(ev.__dict__);

@app.route("/eventos/<int:id>/", methods=["PATCH"])
def edit_event_parsi(id):
    data = request.get_json();
    ev = get_event_or_404(id);

    if "name" in data.keys():
        name = data.get("name");
        if not name:
            abort(400, "'name' precisa ser informado");
        ev.name = name;
    
    if "local" in data.keys():
        local = data.get("local");
        if not local:
            abort(400, "'local' precisa ser informado");
        ev.local = local;
    
    return jsonify(ev.__dict__);
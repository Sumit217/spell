from spell_correct import getPossibleWords, probableCorrection
from flask import Flask, request, jsonify
import ast, time, json

import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


@app.route('/spellCorrect', methods=['POST'])
def home():
    data = ast.literal_eval(request.get_data().decode('UTF-8'))
    print(data, type(data))
    output = getPossibleWords(data)
    print(output, type(output))
    result = json.dumps(output, default=set_default)

    return result

app.run()
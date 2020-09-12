import os
from collections import defaultdict
from pathlib import Path

from flask import render_template
from flask import Flask
from flask import redirect
from flask import request

import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

NOODS_FILE = 'noods.json'

@app.route('/')
def index():
    nood_data = json.load(open(NOODS_FILE))
    return render_template('index.html', slots=nood_data)

@app.route('/submit', methods=['POST'])
def submit():
    noods = defaultdict(dict)

    for k, v in request.form.items():
        _, index, field = k.split('-')
        noods[index][field] = v

    with open(NOODS_FILE, 'w') as f:
        json.dump(noods, f)

    os.system('python3 eink.py')

    return redirect('/')

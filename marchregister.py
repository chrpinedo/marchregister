#!/usr/bin/env python
# -*- coding: utf-8 -*-

# all the imports
import csv
import re
import sqlite3
import tempfile
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash, send_file

# default configuration
# this configuration options may be overwritten by a external configuration
# file provided by the MARCHREGISTER_SETTINGS variable.
DATABASE = '/tmp/marchregister.db'
DATABASE_SQL = 'marchregister.sql'
DATABASE_TABLE = 'entries'
DATABASE_FIELDS = { 'entries' : ['number', 'name', 'first_lastname',
                                 'second_lastname', 'id_number', 'settlement',
                                 'province', 'sex', 'federated', 'club', 
                                 'email', 'born_date', 'registry_date',
                                 'registry_time']}
CSV_FILE = 'registries.csv'
DEBUG = True
SECRET_KEY = '123secret456key'
USERNAME = 'admin'
PASSWORD = 'admin'
HTML_TITLE = 'Gorobel Ibilaldia 2014'
# end of the configuration

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MARCHREGISTER_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(app.config['DATABASE_SQL'], mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def normalize_register():
    normalized = {}
    for field in app.config['DATABASE_FIELDS']['entries']:
        if field == 'name' or field == 'first_lastname' or \
           field == 'second_lastname':
            normalized[field] = request.form[field].strip().title()
        if field == 'id_number':
            if re.match('[0-9]+[A-Z]', request.form[field]):
                normalized[field] = request.form[field].strip()
            else:
                raise
        if field == 'settlement':
            normalized[field] = request.form[field].strip().title()
        if field == 'province':
            if re.match('Alava|Álava|Araba', request.form[field], re.I):
                normalized[field] = 'Araba'
            elif re.match('Bizkaia|Vizcaya', request.form[field], re.I):
                normalized[field] = 'Bizkaia'
            elif re.match('Gipuzkoa|Guipuzcoa|Guipúzcoa', request.form[field],
                          re.I):
                normalized[field] = 'Gipuzkoa'
            elif re.match('Navarra|Nafarroa', request.form[field], re.I):
                normalized[field] = 'Nafarroa'
            elif re.match('Lapurdi', request.form[field], re.I):
                normalized[field] = 'Lapurdi'
            elif re.match('Zuberoa', request.form[field], re.I):
                normalized[field] = 'Zuberoa'
            elif re.match('Nafarroa.*Beherea|Behe.*Nafarroa',
                          request.form[field], re.I):
                normalized[field] = 'Nafarroa Beherea'
            else:
                normalized[field] = request.form[field].strip().title()
        if field == 'sex':
            if re.match('man|woman', request.form[field], re.I):
                normalized[field] = request.form[field].strip().title()
            else:
                raise
        if field == 'federated':
            if re.match('yes|no', request.form[field], re.I):
                normalized[field] = request.form[field].strip().title()
            else:
                raise
        if field == 'club':
            normalized[field] = request.form[field].strip().title()
        if field == 'email':
            if re.match('[^ ]+@[^ ]+\.[^ ]+', request.form[field]):
                normalized[field] = request.form[field].strip().lower()
            else:
                raise
        if field == 'born_date':
            if not re.match('[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}',
                            request.form[field]):
                raise
            day, month, year = request.form[field].split('-', 2)
            if int(month) > 12:
                raise
            if int(day) > 31:
                raise
            normalized[field] = '{}-{}-{}'.format(year, month.rjust(2, '0'),
                                                  day.rjust(2, '0'))
    return normalized

@app.before_request
def before_request():
    g.db = connect_db()
    g.db.row_factory = sqlite3.Row

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        entry = normalize_register()
        matches = query_db('select * from entries where id_number = ?', 
                           [entry['id_number']])
        if matches:
            flash('Error. El usuario ya esta registrado con numero de dorsal %s ' % (matches[0]['number']))
            return render_template('layout.html')
        cur = g.db.execute('insert into entries (name, first_lastname, '
                     'second_lastname, id_number, settlement, province, sex, '
                     'federated, club, email, born_date) values (?, ?, ?, ?, '
                     '?, ?, ?, ?, ?, ?, ?)', [entry['name'],
                     entry['first_lastname'], entry['second_lastname'],
                     entry['id_number'], entry['settlement'],
                     entry['province'], entry['sex'], entry['federated'],
                     entry['club'], entry['email'], entry['born_date']])
        g.db.commit()
        matches = query_db('select * from entries where id_number = ?', 
                           [entry['id_number']])
        flash('Registrado con numero de dorsal %s ' % (matches[0]['number']))
        return render_template('layout.html')

@app.route('/registered', methods=['GET'])
def registered():
    pass

@app.route('/list')
def list():
    entries = query_db('select number, name, first_lastname, second_lastname '
                       ' from entries')
    return render_template('list.html', entries=entries)

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'GET':
        return render_template('download.html')
    elif request.method == 'POST':
        if request.form['username'] == app.config['USERNAME'] and \
           request.form['password'] == app.config['PASSWORD']:
            csvf = open(app.config['CSV_FILE'], 'w')
            wr = csv.DictWriter(csvf, app.config['DATABASE_FIELDS']['entries'])
            wr.writerow(dict(zip(app.config['DATABASE_FIELDS']['entries'],
                                 app.config['DATABASE_FIELDS']['entries'])))
            entries = query_db('select * from entries')
            for entry in entries:
                temp = {}
                for field in app.config['DATABASE_FIELDS']['entries']:
                    temp[field] = entry[field]
                wr.writerow(temp)
            csvf.close()
            csvf = open(app.config['CSV_FILE'], 'r')
            return send_file(csvf, as_attachment=True,
                             attachment_filename="registros.csv")
        else:
            flash('Error. Usuario y/o clave incorrecta.')
            return redirect(url_for('download'))


if __name__ == '__main__':
    if app.config['DEBUG'] is True:
        app.debug = True
    app.run()

# vim: ts=8 sts=4 sw=4 et

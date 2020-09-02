from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

import pymysql
import requests

db_user = 'root'
db_password = '12345'
db_host = 'localhost:3306'
db_name = 'todo'

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(db_user, db_password, db_host, db_name)

db = SQLAlchemy(app)

base_url = 'http://localhost:5000'
api_url = '/api/todo'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)


class TodoForm(FlaskForm):
    todo_text = StringField('New todo item', validators=[DataRequired()])


@app.route('/api/todo', methods=['GET'])
def get_all_todos():
    todos = Todo.query.all()
    output = []

    for todo in todos:
        todo_data = {'id': todo.id, 'text': todo.text, 'complete': todo.complete}
        output.append(todo_data)

    return jsonify({'todos': output})


@app.route('/api/todo/<todo_id>', methods=['GET'])
def get_one_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        return jsonify({'message': 'No todo found!'})

    todo_data = {'id': todo.id, 'text': todo.text, 'complete': todo.complete}

    return jsonify(todo_data)


@app.route('/api/todo', methods=['POST'])
def create_todo():
    data = request.get_json()

    new_todo = Todo(text=data['text'], complete=False)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': "Todo created!"})


@app.route('/api/todo/<todo_id>', methods=['PUT'])
def complete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        return jsonify({'message': 'No todo found!'})

    todo.complete = True
    db.session.commit()

    return jsonify({'message': 'Todo item has been completed!'})


@app.route('/api/todo/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        return jsonify({'message': 'No todo found!'})

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo item deleted!'})


@app.route('/', methods=['GET', 'POST'])
def get_index():
    form = TodoForm()

    if form.validate_on_submit():
        td_item = Todo(text=form.todo_text.data, complete=False)
        db.session.add(td_item)
        db.session.commit()

    # make API call to the /api/todo endpoint
    url = '{}{}'.format(base_url, api_url)
    resp = requests.get(url)

    # check response code
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('GET {} {}'.format(url, resp.status_code))

    # Ok. Then continue...
    todos = resp.json()['todos']

    return render_template("list.html", items=todos, form=form)


@app.route('/delete/<item_id>', methods=['GET'])
def delete_item(item_id):
    # make API call to the /api/todo/id endpoint
    url = '{}{}/{}'.format(base_url, api_url, item_id)
    resp = requests.delete(url)

    # check response code
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('DELETE {} {}'.format(url, resp.status_code))

    return redirect(base_url)


if __name__ == '__main__':
    app.run(debug=True)

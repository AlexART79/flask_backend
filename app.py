
from flask import Flask, request, jsonify, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql

from db_config import db_name, db_host, db_password, db_user

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(db_user, db_password, db_host, db_name)

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)


@app.route('/api/todo', methods=['GET'])
def get_all_todos():
    todos = Todo.query.order_by(Todo.complete)
    output = []

    for todo in todos:
        todo_data = {'id': todo.id, 'text': todo.text, 'complete': todo.complete}
        output.append(todo_data)

    resp = make_response(jsonify({'todos': output}))
    return resp


@app.route('/api/todo/<todo_id>', methods=['GET'])
def get_one_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        resp = make_response(jsonify({'message': 'No todo found!'}))
        return resp

    todo_data = {'id': todo.id, 'text': todo.text, 'complete': todo.complete}

    resp = make_response(jsonify(todo_data))
    return resp


@app.route('/api/todo', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = Todo(text=data['text'], complete=False)
    db.session.add(new_todo)
    db.session.commit()

    resp = make_response(jsonify({'message': "Todo created!"}))
    return resp


@app.route('/api/todo/<todo_id>', methods=['PUT'])
def complete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        resp = make_response(jsonify({'message': 'No todo found!'}))
        return resp

    todo.complete = not todo.complete
    db.session.commit()

    resp = make_response(jsonify({'message': 'Todo item has been completed!'}))
    return resp


@app.route('/api/todo/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        resp = make_response(jsonify({'message': 'No todo found!'}))
        return resp

    db.session.delete(todo)
    db.session.commit()

    resp = make_response(jsonify({'message': 'Todo item deleted!'}))
    return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

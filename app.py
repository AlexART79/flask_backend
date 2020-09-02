from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql

db_user = 'root'
db_password = '12345'
db_host = 'localhost:3306'
db_name = 'todo'

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(db_user, db_password, db_host, db_name)

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)


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


if __name__ == '__main__':
    app.run(debug=True)

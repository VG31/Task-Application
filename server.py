from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL

import raft

# Define constants for task statuses
TODO = 'TODO'
IN_PROGRESS = 'IN_PROGRESS'
COMPLETED = 'COMPLETED'

# Initialize Flask app
app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'tasks'
mysql = MySQL(app)


# Define a class to represent a Task
class Task:
    number_tasks = 0

    def __init__(self, id, title, description, status=TODO):
        self.id = id
        self.title = title
        self.description = description
        self.status = status

# Define the root route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Define API endpoints for task management
@app.route("/tasks", methods=['GET'])
def get_tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    serialized_tasks = [{"id": task[0], "title": task[1], "description": task[2], "status": task[3]} for task in tasks]
    return jsonify(serialized_tasks)

@app.route("/tasks", methods=['POST'])
def create_task():
    data = request.json
    title = data['title']
    description = data['description']
    status = data.get('status', TODO)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s)", (title, description, status))
    mysql.connection.commit()
    cur.close()
    Task.number_tasks += 1
    return "Task created successfully", 201

@app.route("/tasks/<int:task_id>", methods=['GET'])
def get_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()
    cur.close()
    if task:
        return jsonify({"id": task[0], "title": task[1], "description": task[2], "status": task[3]})
    else:
        return "Task not found", 404

@app.route("/tasks/<int:task_id>", methods=['PUT'])
def update_task(task_id):
    data = request.json
    title = data.get('title')
    description = data.get('description')
    status = data.get('status')
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET title = %s, description = %s, status = %s WHERE id = %s", (title, description, status, task_id))
    mysql.connection.commit()
    cur.close()
    return "Task updated successfully"

@app.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cur.close()
    ##raft.start_raft(Task.number_tasks)
    ##Task.number_tasks -= 1
    return "Task deleted successfully", 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

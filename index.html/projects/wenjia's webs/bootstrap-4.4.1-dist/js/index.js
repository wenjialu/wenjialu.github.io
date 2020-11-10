import React, { useState } from "react";
import ReactDOM from "react-dom";

const Task = ({ title, due, description }) => (
  <div className="task">
    <h1>{title}</h1>
    <em>{due}</em>
    <p>{description}</p>
  </div>
);

const TaskInput = ({ onCreate }) => {
  const [title, setTitle] = useState("");
  const [due, setDue] = useState("");
  const [description, setDescription] = useState("");
  const [contentHeight, setContentHeight] = useState(40);

  return (
    <div className="task input">
      <input
        type="text"
        placeholder="Task title"
        className="title"
        value={title}
        onChange={e => setTitle(e.target.value)}
      ></input>
      <input
        type="text"
        placeholder="Due date"
        className="due"
        value={due}
        onChange={e => setDue(e.target.value)}
      ></input>
      <textarea
        className="description"
        placeholder="Description..."
        value={description}
        style={{ height: `${contentHeight}px` }}
        onChange={e => {
          setDescription(e.target.value);
          setContentHeight(e.target.scrollHeight);
        }}
      ></textarea>
      <button
        onClick={() => {
          onCreate({
            title,
            due,
            description
          });
          setTitle("");
          setDue("");
          setDescription("");
          setContentHeight(40);
        }}
      >
        Create
      </button>
    </div>
  );
};

const App = () => {
  const [tasks, setTasks] = useState([]);
  return (
    <main>
      <h1>Tasks</h1>
      <TaskInput onCreate={task => setTasks([task, ...tasks])} />
      {tasks.map(t => (
        <Task {...t} />
      ))}
    </main>
  );
};

ReactDOM.render(<App />, document.getElementById("root"));

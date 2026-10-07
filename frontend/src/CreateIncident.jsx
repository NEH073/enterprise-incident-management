import { useState } from "react";
import axios from "axios";

function CreateIncident({ onIncidentCreated }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("Medium");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("token");

      await axios.post(
        "http://127.0.0.1:8000/incidents",
        {
          title,
          description,
          priority,
          status: "Open",
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setTitle("");
      setDescription("");
      setPriority("Medium");

      onIncidentCreated();
    } catch (error) {
      console.error("Error creating incident:", error);
      alert("Failed to create incident");
    }
  };

  return (
    <div>
      <h2>Create Incident</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Title</label>
          <br />
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <br />

        <div>
          <label>Description</label>
          <br />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>

        <br />

        <div>
          <label>Priority</label>
          <br />

          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
            <option value="Critical">Critical</option>
          </select>
        </div>

        <br />

        <button type="submit">Create Incident</button>
      </form>
    </div>
  );
}

export default CreateIncident;
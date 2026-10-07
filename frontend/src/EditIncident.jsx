
import { useState } from "react";
import axios from "axios";

function EditIncident({ incident, onIncidentUpdated, onCancel }) {
  const [title, setTitle] = useState(incident.title);
  const [description, setDescription] = useState(incident.description);
  const [priority, setPriority] = useState(incident.priority);
  const [status, setStatus] = useState(incident.status);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("token");

      await axios.put(
        `http://127.0.0.1:8000/incidents/${incident.id}`,
        {
          title,
          description,
          priority,
          status,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      onIncidentUpdated();
    } catch (error) {
      console.error("Error updating incident:", error);
      alert("Failed to update incident");
    }
  };

  return (
    <div>
      <h2>Edit Incident #{incident.id}</h2>

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

        <div>
          <label>Status</label>
          <br />
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="Open">Open</option>
            <option value="In Progress">In Progress</option>
            <option value="Resolved">Resolved</option>
            <option value="Closed">Closed</option>
          </select>
        </div>

        <br />

        <button type="submit">Update Incident</button>

        <button type="button" onClick={onCancel}>
          Cancel
        </button>
      </form>
    </div>
  );
}

export default EditIncident;

 
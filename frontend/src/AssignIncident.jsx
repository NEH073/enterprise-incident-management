
import { useEffect, useState } from "react";
import axios from "axios";

function AssignIncident({ incident, onAssigned, onCancel }) {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(
    incident.assigned_to ?? ""
  );

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const token = localStorage.getItem("token");

        const response = await axios.get(
          "http://127.0.0.1:8000/users",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        setUsers(response.data);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, []);

  const handleAssign = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("token");

      await axios.put(
        `http://127.0.0.1:8000/incidents/${incident.id}/assign`,
        {
          assigned_to: selectedUser
            ? Number(selectedUser)
            : null,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      onAssigned();
    } catch (error) {
      console.error("Error assigning incident:", error);
      alert("Failed to assign incident");
    }
  };

  return (
    <div>
      <h2>Assign Incident #{incident.id}</h2>

      <form onSubmit={handleAssign}>
        <label>Assign To</label>
        <br />

        <select
          value={selectedUser}
          onChange={(e) => setSelectedUser(e.target.value)}
        >
          <option value="">Unassigned</option>

          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.username}
            </option>
          ))}
        </select>

        <br />
        <br />

        <button type="submit">Assign</button>

        <button type="button" onClick={onCancel}>
          Cancel
        </button>
      </form>
    </div>
  );
}

export default AssignIncident;


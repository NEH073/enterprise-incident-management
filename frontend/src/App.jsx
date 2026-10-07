
import { useEffect, useState } from "react";
import axios from "axios";
import Login from "./Login";
import Register from "./Register";
import CreateIncident from "./CreateIncident";
import EditIncident from "./EditIncident";
import AssignIncident from "./AssignIncident";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    Boolean(localStorage.getItem("token"))
  );

  const [showRegister, setShowRegister] = useState(false);
  const [incidents, setIncidents] = useState([]);
  const [editingIncident, setEditingIncident] = useState(null);
  const [assigningIncident, setAssigningIncident] = useState(null);
  const [userRole, setUserRole] = useState("");

  const fetchIncidents = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get(
        "http://127.0.0.1:8000/incidents",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setIncidents(response.data);
    } catch (error) {
      console.error("Error fetching incidents:", error);
    }
  };

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get(
        "http://127.0.0.1:8000/me",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setUserRole(response.data.role);
    } catch (error) {
      console.error("Error fetching user profile:", error);
    }
  };

  const deleteIncident = async (incidentId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this incident?"
    );

    if (!confirmed) return;

    try {
      const token = localStorage.getItem("token");

      await axios.delete(
        `http://127.0.0.1:8000/incidents/${incidentId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      fetchIncidents();
    } catch (error) {
      console.error("Error deleting incident:", error);
      alert("Failed to delete incident");
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    setUserRole("");
  };

  useEffect(() => {
    if (!isLoggedIn) return;

    fetchIncidents();
    fetchUserProfile();
  }, [isLoggedIn]);

  if (!isLoggedIn) {
    if (showRegister) {
      return (
        <Register
          onRegistered={() => setShowRegister(false)}
          onBackToLogin={() => setShowRegister(false)}
        />
      );
    }

    return (
      <div>
        <Login onLogin={() => setIsLoggedIn(true)} />

        <button onClick={() => setShowRegister(true)}>
          Create Account
        </button>
      </div>
    );
  }

  if (editingIncident) {
    return (
      <div>
        <EditIncident
          incident={editingIncident}
          onIncidentUpdated={() => {
            setEditingIncident(null);
            fetchIncidents();
          }}
          onCancel={() => setEditingIncident(null)}
        />
      </div>
    );
  }

  if (assigningIncident) {
    return (
      <div>
        <AssignIncident
          incident={assigningIncident}
          onAssigned={() => {
            setAssigningIncident(null);
            fetchIncidents();
          }}
          onCancel={() => setAssigningIncident(null)}
        />
      </div>
    );
  }

  return (
    <div>
      <h1>Enterprise Incident Management</h1>

      <p>Welcome to the Incident Management Dashboard</p>

      <button onClick={logout}>Logout</button>

      <p>
        Role: <strong>{userRole}</strong>
      </p>

      <CreateIncident onIncidentCreated={fetchIncidents} />

      <h2>Incidents</h2>

      <p>Total incidents: {incidents.length}</p>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Description</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Assigned To</th>
            <th>Action</th>

            {userRole === "admin" && <th>Admin Action</th>}
          </tr>
        </thead>

        <tbody>
          {incidents.map((incident) => (
            <tr key={incident.id}>
              <td>{incident.id}</td>
              <td>{incident.title}</td>
              <td>{incident.description}</td>
              <td>{incident.priority}</td>
              <td>{incident.status}</td>
              <td>
                {incident.assigned_username ?? "Unassigned"}
              </td>

              <td>
                <button
                  onClick={() => setEditingIncident(incident)}
                >
                  Edit
                </button>
              </td>

              {userRole === "admin" && (
                <td>
                  <button
                    onClick={() => setAssigningIncident(incident)}
                  >
                    Assign
                  </button>

                  {" "}

                  <button
                    onClick={() => deleteIncident(incident.id)}
                  >
                    Delete
                  </button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;


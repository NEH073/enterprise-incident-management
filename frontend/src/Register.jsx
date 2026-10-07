
import { useState } from "react";
import axios from "axios";

function Register({ onRegistered, onBackToLogin }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      await axios.post("http://127.0.0.1:8000/register", {
        username,
        email,
        password,
      });

      alert("Registration successful! Please login.");
      onRegistered();
    } catch (error) {
      alert(
        error.response?.data?.detail || "Registration failed"
      );
    }
  };

  return (
    <div>
      <h2>Register</h2>

      <form onSubmit={handleRegister}>
        <div>
          <label>Username</label>
          <br />
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <br />

        <div>
          <label>Email</label>
          <br />
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <br />

        <div>
          <label>Password</label>
          <br />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <br />

        <button type="submit">Register</button>
      </form>

      <br />

      <button onClick={onBackToLogin}>
        Back to Login
      </button>
    </div>
  );
}

export default Register;

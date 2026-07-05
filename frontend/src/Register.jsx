import { useState } from "react";
import axios from "axios";

function Register({ onSwitchToLogin }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("researcher");
  const [message, setMessage] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/auth/register", {
        name,
        email,
        password,
        role,
      });

      setMessage(`Registered successfully: ${response.data.email}`);
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.detail || "Registration failed");
      } else {
        setMessage("Could not connect to server");
      }
    }
  };

  return (
    <div style={{ maxWidth: "320px", margin: "80px auto", fontFamily: "sans-serif" }}>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <div style={{ marginBottom: "10px" }}>
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            style={{ width: "100%", padding: "8px" }}
            required
          />
        </div>
        <div style={{ marginBottom: "10px" }}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ width: "100%", padding: "8px" }}
            required
          />
        </div>
        <div style={{ marginBottom: "10px" }}>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: "100%", padding: "8px" }}
            required
          />
        </div>
        <div style={{ marginBottom: "10px" }}>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            style={{ width: "100%", padding: "8px" }}
          >
            <option value="researcher">Researcher</option>
            <option value="startup_founder">Startup Founder</option>
            <option value="innovation_manager">Innovation Manager</option>
            <option value="admin">Administrator</option>
          </select>
        </div>
        <button type="submit" style={{ width: "100%", padding: "8px" }}>
          Register
        </button>
      </form>

      {message && <p style={{ marginTop: "12px" }}>{message}</p>}

      <p style={{ marginTop: "16px", fontSize: "14px" }}>
        Already have an account?{" "}
        <span
          style={{ color: "#4f9dff", cursor: "pointer" }}
          onClick={onSwitchToLogin}
        >
          Login here
        </span>
      </p>
    </div>
  );
}

export default Register;
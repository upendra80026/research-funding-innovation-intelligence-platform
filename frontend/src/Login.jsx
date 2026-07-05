import { useState } from "react";
import axios from "axios";

function Login({ onLoginSuccess, onSwitchToRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [token, setToken] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/auth/login", {
        email: email,
        password: password,
      });

     setToken(response.data.access_token);
     setMessage("Login successful!");
     onLoginSuccess(response.data.access_token);
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.detail || "Login failed");
      } else {
        setMessage("Could not connect to server");
      }
    }
  };

  return (
    <div style={{ maxWidth: "320px", margin: "80px auto", fontFamily: "sans-serif" }}>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
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
        <button type="submit" style={{ width: "100%", padding: "8px" }}>
          Login
        </button>
      </form>
      <p style={{ marginTop: "16px", fontSize: "14px" }}>
        Don't have an account?{" "}
        <span
          style={{ color: "#4f9dff", cursor: "pointer" }}
          onClick={onSwitchToRegister}
        >
          Register here
        </span>
      </p>
      {message && <p style={{ marginTop: "12px" }}>{message}</p>}

      {token && (
        <div style={{ marginTop: "12px", wordBreak: "break-all", fontSize: "12px" }}>
          <strong>Token:</strong> {token}
        </div>
      )}
    </div>
  );
}

export default Login;
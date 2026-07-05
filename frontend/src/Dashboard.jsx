import { useEffect, useState } from "react";
import axios from "axios";

function Dashboard({ token, onLogout }) {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/auth/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setProfile(response.data);
      } catch (err) {
        setError("Could not load profile");
      }
    };

    fetchProfile();
  }, [token]);

  return (
    <div style={{ maxWidth: "400px", margin: "80px auto", fontFamily: "sans-serif" }}>
      <h2>Dashboard</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {profile ? (
        <div>
          <p><strong>Email:</strong> {profile.email}</p>
          <p><strong>Role:</strong> {profile.role}</p>
        </div>
      ) : (
        !error && <p>Loading...</p>
      )}

      <button onClick={onLogout} style={{ marginTop: "20px", padding: "8px 16px" }}>
        Logout
      </button>
    </div>
  );
}
export default Dashboard;
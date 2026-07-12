import { useEffect, useState } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

function PublicationTrend() {
  const [data, setData] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchTrend = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/profile/publications/trend"
        );
        setData(response.data);
      } catch (err) {
        setError("Could not load publication trend");
      }
    };

    fetchTrend();
  }, []);

  return (
    <div style={{ marginTop: "24px" }}>
      <h3>Publication Trend</h3>
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!error && data.length === 0 && (
        <p style={{ color: "gray" }}>No publication data yet.</p>
      )}

      {data.length > 0 && (
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={data}>
            <XAxis dataKey="year" stroke="#ccc" />
            <YAxis allowDecimals={false} stroke="#ccc" />
            <Tooltip />
            <Bar dataKey="count" fill="#8884d8" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

export default PublicationTrend;
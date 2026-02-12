import { useState } from "react";

export default function ManufacturerPanel() {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const generateQR = async () => {
  setLoading(true);
  setResponse(null);

  const res = await fetch("http://127.0.0.1:5000/generate", {
    method: "POST"
  });

  const data = await res.json();
  setResponse(data);
  setLoading(false);
};


  return (
    <div className="card">
      <h2>Generate Serialized QR</h2>

      <button onClick={generateQR} disabled={loading}>
        {loading ? "Generating..." : "Generate & Register"}
      </button>

      {response && (
        <div className="result-success">
          <p><strong>ID:</strong> {response.id}</p>
          <p>Registered on Blockchain</p>
        </div>
      )}
    </div>
  );
}

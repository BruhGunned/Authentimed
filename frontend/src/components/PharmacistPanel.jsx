import { useState } from "react";
import ResultCard from "./ResultCard";

const API_BASE = "http://127.0.0.1:5000";

export default function PharmacistPanel() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const verify = async () => {
    if (!file) return;

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/pharmacist/verify`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ "Final Verdict": "ERROR", "Message": "Server Error" });
    }

    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Pharmacist Verification</h2>
      <p style={{ marginBottom: "8px", color: "#555" }}>
        Upload image with QR or strip (full pack, QR-only, or strip-only). Same as consumer: one verification per product — if QR was already scanned, scanning the connected strip is flagged (and vice versa).
      </p>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
        style={{ marginBottom: "8px" }}
      />

      <button onClick={verify} disabled={loading}>
        {loading ? "Verifying..." : "Verify Medicine"}
      </button>

      {result && <ResultCard result={result} />}
    </div>
  );
}

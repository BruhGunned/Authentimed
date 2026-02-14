import { useState } from "react";
import ResultCard from "./ResultCard";

const API_BASE = "http://127.0.0.1:5000";

export default function ConsumerPanel() {
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
      const res = await fetch(`${API_BASE}/consumer/verify`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ "Final Verdict": "ERROR", "Message": "Server error" });
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Verify Medicine</h2>
      <p style={{ marginBottom: "12px", color: "#555" }}>
        Upload an image: full package with QR, QR only, or strip. Verification works in all cases. One verification per product — if already verified (e.g. via QR), scanning again (e.g. strip) is flagged.
      </p>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
        style={{ marginBottom: "8px" }}
      />

      <button onClick={verify} disabled={loading}>
        {loading ? "Verifying..." : "Verify"}
      </button>

      {result && <ResultCard result={result} />}
    </div>
  );
}

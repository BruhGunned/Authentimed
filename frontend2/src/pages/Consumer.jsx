import { useState } from "react";
import ResultCard from "../components/ResultCard";
import "../styles/manufacturer.css";

const API_BASE = "http://127.0.0.1:5000";

export default function Consumer() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleVerify = async () => {
    if (!file) {
      alert("Upload medicine image");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(`${API_BASE}/consumer/verify`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);

    } catch (err) {
      setResult({
        "Final Verdict": "ERROR",
        "Message": "Backend connection failed",
      });
    }

    setLoading(false);
  };

  return (
    <div className="manufacturer-wrapper">

      {/* Header */}
      <div className="manufacturer-header">
        <h1>Consumer Portal</h1>
        <p>
          Instantly verify product authenticity and inspect blockchain
          scan history before use.
        </p>
      </div>

      {/* Main Content */}
      <div className="manufacturer-content">

        {/* Upload Section */}
        <div className="upload-section">
          <h3>Step 1 — Upload Medicine Image</h3>

          <input
            type="file"
            id="consumerUpload"
            accept="image/*"
            style={{ display: "none" }}
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button
            className="primary-btn"
            onClick={() => document.getElementById("consumerUpload").click()}
          >
            {file ? "File Selected ✓" : "Upload Medicine Image"}
          </button>
        </div>

        {/* Action Section */}
        <div className="action-section">
          <h3>Step 2 — Check Authenticity</h3>

          <button
            className="primary-btn"
            onClick={handleVerify}
            disabled={loading}
          >
            {loading ? "Verifying..." : "Verify Product"}
          </button>
        </div>

      </div>

      {/* Result Section */}
      {result && (
        <div className="manufacturer-result">
          <ResultCard result={result} />
        </div>
      )}

    </div>
  );
}

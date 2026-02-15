import { useState } from "react";
import "../styles/manufacturer.css";

const API_BASE = "http://127.0.0.1:5000";

export default function Manufacturer() {
  const [templateFile, setTemplateFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!templateFile) {
      alert("Upload packaging template");
      return;
    }

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", templateFile);

    try {
      const res = await fetch(`${API_BASE}/manufacturer/generate`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Server connection failed" });
    }

    setLoading(false);
  };

  return (
    <div className="manufacturer-wrapper">

      <div className="manufacturer-header">
        <h1>Manufacturer Portal</h1>
        <p>
          Register product batches and generate blockchain-authenticated QR codes
          for secure pharmaceutical distribution.
        </p>
      </div>

      <div className="manufacturer-content">

        {/* Upload Section */}
        <div className="upload-section">
          <h3>Step 1 — Upload Packaging Template</h3>

          <input
            type="file"
            id="fileUpload"
            style={{ display: "none" }}
            onChange={(e) => setTemplateFile(e.target.files[0])}
          />

          <button
            className="primary-btn"
            onClick={() => document.getElementById("fileUpload").click()}
          >
            {templateFile ? "File Selected ✓" : "Upload Template"}
          </button>
        </div>

        {/* Action Section */}
        <div className="action-section">
          <h3>Step 2 — Generate & Register</h3>

          <button
            className="primary-btn"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? "Registering..." : "Generate & Register On-Chain"}
          </button>
        </div>

      </div>

      {/* Result Section */}
      {result && (
        <div className="manufacturer-result">
          {result.error ? (
            <div className="result-error">
              <h3>Registration Failed</h3>
              <p>{result.error}</p>
            </div>
          ) : (
            <div className="result-success">
              <h3>Product Registered Successfully</h3>

              <p>
                <strong>ID:</strong> {result["Product ID"]}
              </p>

              <p>
                <strong>Status:</strong>{" "}
                {result.Status || result["Status"] || "Registered"}
              </p>

              {result["Packaged Image"] && (
                <img
                  src={`${API_BASE}/${result["Packaged Image"]}`}
                  alt="Generated Packaging"
                  style={{ width: "300px", marginTop: "20px" }}
                />
              )}
            </div>
          )}
        </div>
      )}

    </div>
  );
}

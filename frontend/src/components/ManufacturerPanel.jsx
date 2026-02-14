import { useState } from "react";
import ResultCard from "./ResultCard";

export default function ManufacturerPanel() {
  const [account, setAccount] = useState("");
  const [templateFile, setTemplateFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleOnboard = async () => {
    if (!account || !templateFile) return;

    const formData = new FormData();
    formData.append("account", account);
    formData.append("file", templateFile);

    const res = await fetch("http://127.0.0.1:5000/manufacturer/onboard", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
  };

  const handleGenerate = async () => {
    if (!account) return;

    const formData = new FormData();
    formData.append("account", account);

    const res = await fetch("http://127.0.0.1:5000/manufacturer/generate", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="card">
      <h2>Manufacturer Dashboard</h2>

      <input
        type="text"
        placeholder="Manufacturer Account"
        value={account}
        onChange={(e) => setAccount(e.target.value)}
      />

      <hr className="divider" />

      <h3>Step 1 — Onboard Manufacturer</h3>

      <input
        type="file"
        onChange={(e) => setTemplateFile(e.target.files[0])}
      />

      <button onClick={handleOnboard}>
        Onboard & Register Template
      </button>

      <hr className="divider" />

      <h3>Step 2 — Generate Product</h3>

      <button onClick={handleGenerate}>
        Generate QR & Register Product
      </button>

      <ResultCard result={result} />
    </div>
  );
}

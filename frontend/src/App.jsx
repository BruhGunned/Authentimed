import { useState } from "react";
import ManufacturerPanel from "./components/ManufacturerPanel";
import ConsumerPanel from "./components/ConsumerPanel";

export default function App() {
  const [activeTab, setActiveTab] = useState("manufacturer");

  return (
    <div className="app">
      <header className="header">
        <h1>Authentimed</h1>
        <p>AI + Blockchain Powered Drug Verification</p>
      </header>

      <div className="tabs">
        <button
          className={activeTab === "manufacturer" ? "active" : ""}
          onClick={() => setActiveTab("manufacturer")}
        >
          Manufacturer
        </button>
        <button
          className={activeTab === "consumer" ? "active" : ""}
          onClick={() => setActiveTab("consumer")}
        >
          Consumer
        </button>
      </div>

      <div className="panel">
        {activeTab === "manufacturer" && <ManufacturerPanel />}
        {activeTab === "consumer" && <ConsumerPanel />}
      </div>
    </div>
  );
}

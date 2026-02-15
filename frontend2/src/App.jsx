import { useState } from "react";
import ManufacturerPanel from "./components/ManufacturerPanel";
import PharmacistPanel from "./components/PharmacistPanel";
import ConsumerPanel from "./components/ConsumerPanel";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";
import DashboardSelect from "./pages/DashboardSelect";
import Manufacturer from "./pages/Manufacturer";
import Consumer from "./pages/Consumer";
import Pharmacist from "./pages/Pharmacist";


export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/dashboard" element={<DashboardSelect />} />
        <Route path="/manufacturer" element={<Manufacturer />} />
        <Route path= "/consumer" element={<Consumer/>}/>
        
        <Route path= "/pharmacist" element={<Pharmacist/>}/>
        
      </Routes>
    </Router>
  );
}
/*
<Route path= "/consumer" element={<Consumer/>}/>
        <Route path= "/pharmacist" element={<Pharmacist/>}/>*/
/*export default function App() {
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
          className={activeTab === "pharmacist" ? "active" : ""}
          onClick={() => setActiveTab("pharmacist")}
        >
          Pharmacist
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
        {activeTab === "pharmacist" && <PharmacistPanel />}
        {activeTab === "consumer" && <ConsumerPanel />}
      </div>
    </div>
  );
}
*/
import { useNavigate } from "react-router-dom";

export default function DashboardSelect() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: "60px", textAlign: "center" }}>
      <h1>Select Role</h1>

      <div style={{ marginTop: "40px", display: "flex", gap: "30px", justifyContent: "center" }}>
        <button onClick={() => navigate("/manufacturer")}>Manufacturer</button>
        <button onClick={() => navigate("/pharmacist")}>Pharmacist</button>
        <button onClick={() => navigate("/consumer")}>Consumer</button>
      </div>
    </div>
  );
}

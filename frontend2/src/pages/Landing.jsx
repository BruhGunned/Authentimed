import { useNavigate } from "react-router-dom";
import "../styles/landing.css";
import pharmacistIcon from "../assets/pharmacist.png";
import personIcon from"../assets/Person.png";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="landing">

      <div className="hero">

        <div className="hero-left">
          <div className="tag">SECURE PHARMACEUTICAL INFRASTRUCTURE</div>

          <h1>
            Authenti<span>MED</span>
          </h1>

          <p>
            AI-powered packaging verification combined with blockchain-backed
            authentication infrastructure for pharmaceutical supply chains.
          </p>
        </div>

        <div className="hero-right" />
      </div>

      <div className="roles">
        <h2>Select Your Role</h2>

        <div className="role-row">

          <div className="role-card" onClick={() => navigate("/manufacturer")}>
            <img 
    src="https://img.icons8.com/ios-filled/100/22c55e/factory.png"
    alt="Manufacturer Icon"
    className="role-icon"
  />
            <h3>Manufacturer</h3>
            <p>Register medicine batches on-chain.</p>
          </div>

          <div className="role-card" onClick={() => navigate("/pharmacist")}>
            <img
    src={pharmacistIcon}
    alt="Pharmacist Icon"
    className="role-icon"
  />
            <h3>Pharmacist</h3>
            <p>Activate and verify distributed products.</p>
          </div>

          <div className="role-card" onClick={() => navigate("/consumer")}>
            <img
    src={personIcon}
    alt="person Icon"
    className="role-icon"
  />
            <h3>Consumer</h3>
            <p>Check authenticity and scan history.</p>
          </div>

        </div>
      </div>

    </div>
  );
}

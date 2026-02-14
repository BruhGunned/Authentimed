const API_BASE = "http://127.0.0.1:5000";

export default function ResultCard({ result }) {
  if (!result) return null;

  const verdict = result["Final Verdict"];
  const status = result["Status"];

  let title = "";
  let cardClass = "result-neutral";

  // -----------------------------
  // Manufacturer Registration
  // -----------------------------
  if (status === "Registered On-Chain") {
    title = "✔ PRODUCT REGISTERED";
    cardClass = "result-success";
  }

  // -----------------------------
  // Verification Logic
  // -----------------------------
  else if (verdict === "GENUINE") {
    title = "✔ GENUINE PRODUCT";
    cardClass = "result-success";
  }

  else if (verdict === "VERIFIED") {
    title = "✔ VERIFIED";
    cardClass = "result-success";
  }

  else if (verdict === "UNVERIFIED") {
    title = "⚠ NOT YET PHARMACIST VERIFIED";
    cardClass = "result-warning";
  }

  else if (verdict === "COUNTERFEIT") {
    title = "✖ COUNTERFEIT";
    cardClass = "result-fail";
  }

  const hasLinked = result["Product ID"] && result["Strip code"];

  return (
    <div className={`result-card ${cardClass}`}>
      <h2>{title}</h2>

      {hasLinked && (
        <p className="product-identity" style={{ marginBottom: "4px" }}>
          <strong>Product:</strong> {result["Product ID"]} <span style={{ color: "#666" }}>(QR)</span>
          {" · "}
          <strong>{result["Strip code"]}</strong> <span style={{ color: "#666" }}>(strip)</span>
        </p>
      )}
      {result["Product ID"] && !result["Strip code"] && (
        <p><strong>Product ID:</strong> {result["Product ID"]}</p>
      )}
      {result["Strip code"] && !result["Product ID"] && (
        <p><strong>Strip code:</strong> {result["Strip code"]}</p>
      )}

      {result["Linked"] && (
        <p style={{ fontSize: "0.9em", color: "#555" }}>{result["Linked"]}</p>
      )}

      {result["Reason"] && (
        <p><strong>Reason:</strong> {result["Reason"]}</p>
      )}

      {result["Message"] && (
        <p>{result["Message"]}</p>
      )}

      {result["First Scan Time"] && (
        <p><strong>First Scan:</strong> {String(result["First Scan Time"])}</p>
      )}

      {result["Factor"] && (
        <p><strong>Verified via:</strong> {result["Factor"] === "qr" ? "QR" : "Strip code"}</p>
      )}

      {result["Flag"] && (
        <p style={{ color: "#c00" }}><strong>Flag:</strong> {result["Flag"]}</p>
      )}

      {result["images"] && (
        <div style={{ marginTop: "15px", display: "flex", flexWrap: "wrap", gap: "12px", alignItems: "flex-start" }}>
          {result.images.packaged && (
            <div>
              <strong>Packaged (template + QR)</strong>
              <img
                src={`${API_BASE}${result.images.packaged}`}
                alt="Packaged"
                style={{ width: "250px", display: "block", marginTop: "4px" }}
              />
            </div>
          )}
          {result.images.hidden && (
            <div>
              <strong>Hidden code</strong>
              <img
                src={`${API_BASE}${result.images.hidden}`}
                alt="Hidden"
                style={{ width: "120px", display: "block", marginTop: "4px" }}
              />
            </div>
          )}
          {result.images.red_reveal && (
            <div>
              <strong>Reveals (in folder)</strong>
              <div style={{ display: "flex", gap: "4px", flexWrap: "wrap" }}>
                <img src={`${API_BASE}${result.images.red_reveal}`} alt="Red" style={{ width: "80px", display: "block" }} />
                {result.images.blue_reveal && <img src={`${API_BASE}${result.images.blue_reveal}`} alt="Blue" style={{ width: "80px", display: "block" }} />}
                {result.images.green_reveal && <img src={`${API_BASE}${result.images.green_reveal}`} alt="Green" style={{ width: "80px", display: "block" }} />}
              </div>
            </div>
          )}
        </div>
      )}
      {result["Packaged Image"] && !result["images"] && (
        <img
          src={`${API_BASE}${result["Packaged Image"]}`}
          alt="Packaged"
          style={{ width: "250px", marginTop: "15px" }}
        />
      )}
    </div>
  );
}

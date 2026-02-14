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

  return (
    <div className={`result-card ${cardClass}`}>
      <h2>{title}</h2>

      {result["Product ID"] && (
        <p><strong>Product ID:</strong> {result["Product ID"]}</p>
      )}

      {result["Reason"] && (
        <p><strong>Reason:</strong> {result["Reason"]}</p>
      )}

      {result["Message"] && (
        <p>{result["Message"]}</p>
      )}

      {result["First Scan Time"] && (
        <p><strong>First Scan:</strong> {result["First Scan Time"]}</p>
      )}

      {result["Packaged Image"] && (
        <img
          src={`http://127.0.0.1:5000/${result["Packaged Image"]}`}
          alt="Packaged"
          style={{ width: "250px", marginTop: "15px" }}
        />
      )}
    </div>
  );
}

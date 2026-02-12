export default function ResultCard({ result }) {
  const isGenuine = result["Final Verdict"] === "GENUINE";

  return (
    <div className={`verdict ${isGenuine ? "genuine" : "fake"}`}>
      <h3>{isGenuine ? "GENUINE PRODUCT" : "COUNTERFEIT DETECTED"}</h3>

      <div className="details">
        <p><strong>AI Result:</strong> {result["AI Result"]}</p>
        <p><strong>Blockchain:</strong> {result["Blockchain Result"]}</p>
      </div>
    </div>
  );
}

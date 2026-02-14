export default function ResultCard({ result }) {
  if (!result) return null;

  const verdict = result["Final Verdict"];

  let containerClass = "verdict";
  let heading = "";

  if (verdict === "GENUINE") {
    containerClass += " genuine";
    heading = "✔ GENUINE PRODUCT";
  } else if (verdict === "VERIFIED") {
    containerClass += " genuine";
    heading = "✔ VERIFIED PRODUCT";
  } else if (verdict === "REPLAYED") {
    containerClass += " replayed";
    heading = "⚠ REPLAY DETECTED";
  } else if (verdict === "UNVERIFIED") {
    containerClass += " replayed";
    heading = "⚠ NOT YET VERIFIED BY PHARMACIST";
  } else {
    containerClass += " fake";
    heading = "✖ COUNTERFEIT DETECTED";
  }

  return (
    <div className={containerClass}>
      <h3>{heading}</h3>

      <div className="details">
        {Object.entries(result).map(([key, value]) => {
          if (key === "Final Verdict") return null;

          return (
            <p key={key}>
              <strong>{key}:</strong> {String(value)}
            </p>
          );
        })}
      </div>
    </div>
  );
}

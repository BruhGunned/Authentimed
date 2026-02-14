const API_BASE = "http://127.0.0.1:5000";

export default function ResultCard({ result }) {
  if (!result) return null;

  const verdict = result["Final Verdict"];
  const images = result.images;

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
  } else if (verdict) {
    containerClass += " fake";
    heading = "✖ COUNTERFEIT DETECTED";
  }

  return (
    <div className={containerClass}>
      {heading && <h3>{heading}</h3>}

      <div className="details">
        {Object.entries(result).map(([key, value]) => {
          if (key === "Final Verdict" || key === "images") return null;
          if (typeof value === "object") return null;
          return (
            <p key={key}>
              <strong>{key}:</strong> {String(value)}
            </p>
          );
        })}
      </div>

      {/* Image outputs from id_generation, revealer, extractor */}
      {images && (
        <div className="result-images">
          <h4>Generated images (id_generation, revealer)</h4>
          <div className="image-grid">
            {images.packaged && (
              <div>
                <label>Packaged (QR)</label>
                <img src={`${API_BASE}${images.packaged}`} alt="Packaged" />
              </div>
            )}
            {images.hidden && (
              <div>
                <label>Hidden code (id_generation)</label>
                <img src={`${API_BASE}${images.hidden}`} alt="Hidden code" />
              </div>
            )}
            {images.red_reveal && (
              <div>
                <label>Red reveal (revealer)</label>
                <img src={`${API_BASE}${images.red_reveal}`} alt="Red reveal" />
              </div>
            )}
            {images.blue_reveal && (
              <div>
                <label>Blue reveal (revealer)</label>
                <img src={`${API_BASE}${images.blue_reveal}`} alt="Blue reveal" />
              </div>
            )}
            {images.green_reveal && (
              <div>
                <label>Green reveal (revealer)</label>
                <img src={`${API_BASE}${images.green_reveal}`} alt="Green reveal" />
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

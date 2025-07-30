// frontend/js/result.js

document.addEventListener("DOMContentLoaded", () => {
  const resultsSection = document.getElementById("resultsSection");
  const data = JSON.parse(sessionStorage.getItem("analysisResult") || '{}').result || {};
  if (!data) {
    resultsSection.innerHTML = `<p>No data found.</p>`;
    return;
  }

  // 1) RAG indicator
  const rag = data.rag_indicator || 'yellow';
  const ragColors = { green: '#299f4a', yellow: '#f5b100', red: '#e53e3e' };
  const ragLabels = { green: 'High Trust', yellow: 'Medium Trust', red: 'Low Trust' };

  // 2) Source Cross‑Check
  const sources = data.source_cross_check || {};
  const crossList = (sources.matches || [])
    .map(s => `<li>${s}</li>`).join('');

  // 3) Heuristic Indicators
  const h = data.heuristic || {};
  const heurList = `
    <li>Loaded Terms: ${h.loaded_terms.join(', ')}</li>
    <li>Emotion Density: ${h.emotion_density_pct}%</li>
    <li>Subjectivity: ${h.subjectivity_score}</li>
    <li>Passive Voice: ${h.passive_voice_pct}%</li>
  `;

  // 4) Technical Metadata
  const tech = data.technical || {};

  // Build HTML
  resultsSection.innerHTML = `
    <div style="text-align:center; margin-bottom:24px;">
      <span style="display:inline-block;
                 width:24px; height:24px;
                 background:${ragColors[rag]};
                 border-radius:50%;
                 margin-bottom:8px;"></span>
      <h2 style="margin:4px 0;">${ragLabels[rag]}</h2>
    </div>

    <div style="margin-bottom:18px;">
      <h3>🔗 Source Cross‑Check</h3>
      <p>Checked top ${sources.checked} Armenian sources; found matches in:</p>
      <ul>${crossList}</ul>
    </div>

    <div style="margin-bottom:18px;">
      <h3>🧩 Heuristic Indicators</h3>
      <ul>${heurList}</ul>
    </div>

    <div style="margin-bottom:18px;">
      <h3>⚙️ Technical Metadata</h3>
      <ul>
        <li>Method: ${tech.method}</li>
        <li>Sources Checked: ${tech.sources_checked}</li>
      </ul>
    </div>

    <div style="margin-bottom:18px;">
      <h3>🚩 Red Flags (${data.red_flags.length})</h3>
      <ul>${data.red_flags.map(f=>`<li>${f}</li>`).join('')}</ul>
    </div>

    ${
      Array.isArray(data.entities) && data.entities.length && data.entities.some(e => e.name && e.name !== "undefined") ?
      `<div style="margin-bottom:18px;">
        <h3>👥 Key Entities</h3>
        <ul>${data.entities
          .filter(e => e.name && e.name !== "undefined")
          .map(e => `<li><strong>${e.name}</strong> (${e.type})</li>`)
          .join('')}
        </ul>
      </div>` : ""
    }

    <div style="margin-bottom:18px;">
      <h3>📝 Summary</h3>
      <p><b>Credibility Score:</b> ${data.credibility_score ?? "N/A"}<br>${data.summary}</p>
    </div>

    <div style="text-align:right; color:#718096; font-size:0.9em;">
      Analyzed at: ${new Date(data.metadata.processed_at).toLocaleString()}
    </div>
`;

});

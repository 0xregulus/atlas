'use client'

export function ObservabilityPanel({ embedUrl }: { embedUrl?: string }) {
  if (!embedUrl) return null

  return (
    <div className="card">
      <h3>Observability Snapshot</h3>
      <p style={{ color: '#94a3b8' }}>Live Grafana/Prometheus panel (read-only).</p>
      <iframe
        src={embedUrl}
        style={{ width: '100%', height: '320px', border: 'none', borderRadius: '12px', background: '#0f172a' }}
        allowFullScreen
      />
    </div>
  )
}

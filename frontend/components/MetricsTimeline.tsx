'use client'

import type { UsageSummary } from '@/lib/api'

export function MetricsTimeline({ data, error, onRetry }: { data: UsageSummary[] | null; error?: string | null; onRetry?: () => void }) {
  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3>AI Usage (last 24h)</h3>
          <p style={{ color: '#94a3b8' }}>Tokens + latency reported via `/metrics/usage`.</p>
        </div>
        {onRetry && (
          <button onClick={onRetry} style={retryButtonStyle}>
            Refresh
          </button>
        )}
      </div>
      {error && <p style={{ color: '#f87171' }}>{error}</p>}
      {!error && (!data || data.length === 0) && <p style={{ color: '#94a3b8' }}>Connect `CORE_API_BEARER_TOKEN` to view telemetry.</p>}
      {!error && data && data.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {data.map((row) => (
            <div key={row.tenant}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <strong>{row.tenant}</strong>
                <span style={{ color: '#94a3b8' }}>{row.tokens.toLocaleString()} tokens • {row.events} events • {row.latency_ms.toFixed(1)} ms p95</span>
              </div>
              <div style={barTrackStyle}>
                <div style={{ ...barFillStyle, width: `${Math.min(100, (row.tokens / maxTokens(data)) * 100)}%` }} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

const barTrackStyle: React.CSSProperties = {
  width: '100%',
  height: '8px',
  borderRadius: '999px',
  background: 'rgba(148, 163, 184, 0.2)',
  marginTop: '0.25rem',
}

const barFillStyle: React.CSSProperties = {
  height: '100%',
  borderRadius: '999px',
  background: 'linear-gradient(90deg, #3b82f6 0%, #22d3ee 100%)',
}

const retryButtonStyle: React.CSSProperties = {
  borderRadius: '999px',
  padding: '0.35rem 0.9rem',
  border: '1px solid rgba(148,163,184,0.4)',
  background: 'transparent',
  color: '#e2e8f0',
  cursor: 'pointer',
}

function maxTokens(data: UsageSummary[]): number {
  return data.reduce((max, row) => Math.max(max, row.tokens), 1)
}

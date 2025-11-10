'use client'

export function ErrorBanner({ message, onDismiss }: { message: string; onDismiss?: () => void }) {
  if (!message) return null

  return (
    <div className="card" style={{ borderColor: '#f97316', background: 'rgba(251, 146, 60, 0.1)', color: '#f97316' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>⚠️ {message}</span>
        {onDismiss && (
          <button
            onClick={onDismiss}
            style={{ background: 'transparent', border: 'none', color: '#f97316', cursor: 'pointer' }}
          >
            Dismiss
          </button>
        )}
      </div>
    </div>
  )
}

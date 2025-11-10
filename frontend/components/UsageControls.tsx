'use client'

import { useTransition } from 'react'

import { simulateUsage } from '@/app/actions'

export function UsageControls({ tenant, onRefresh, onError }: { tenant: string; onRefresh: () => Promise<void>; onError?: (message: string) => void }) {
  const [isPending, startTransition] = useTransition()

  const handleSimulate = () => {
    startTransition(async () => {
      try {
        await simulateUsage(tenant)
        await onRefresh()
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to simulate usage'
        onError?.(message)
      }
    })
  }

  return (
    <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div>
        <h3>AI Traffic</h3>
        <p style={{ color: '#94a3b8' }}>Trigger a mock LangGraph workflow to exercise the API + billing stack.</p>
      </div>
      <button
        onClick={handleSimulate}
        disabled={isPending}
        style={{
          padding: '0.75rem 1.5rem',
          borderRadius: '999px',
          border: 'none',
          background: '#22c55e',
          color: '#0f172a',
          fontWeight: 600,
          cursor: 'pointer',
        }}
      >
        {isPending ? 'Simulating…' : 'Simulate Usage'}
      </button>
    </div>
  )
}

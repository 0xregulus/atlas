import type { BillingPreview } from '@/lib/api'

export function BillingCard({ billing }: { billing?: BillingPreview }) {
  if (!billing) {
    return null
  }

  return (
    <div className="card">
      <p style={{ textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '0.2em', color: '#94a3b8' }}>Billing</p>
      <h2 style={{ margin: '0.3rem 0', fontSize: '2.5rem' }}>${billing.estimated_amount_usd.toFixed(2)}</h2>
      <p style={{ color: '#94a3b8', margin: 0 }}>Plan: {billing.plan.toUpperCase()}</p>
      <p style={{ color: '#94a3b8', margin: 0 }}>Next charge: {new Date(billing.next_charge_date).toLocaleDateString()}</p>
    </div>
  )
}

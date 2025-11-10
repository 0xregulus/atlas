'use client'

const tenants = [
  { id: 'demo', name: 'Demo Co' },
  { id: 'acme', name: 'Acme Labs' },
  { id: 'globex', name: 'Globex' },
]

export function TenantSwitcher({ activeTenant, onChange }: { activeTenant: string; onChange: (tenant: string) => void }) {
  return (
    <div className="card">
      <h3>Tenant</h3>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        {tenants.map((tenant) => (
          <button
            key={tenant.id}
            onClick={() => onChange(tenant.id)}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: '999px',
              border: '1px solid rgba(148, 163, 184, 0.4)',
              background: activeTenant === tenant.id ? '#2563eb' : 'transparent',
              color: activeTenant === tenant.id ? 'white' : '#e2e8f0',
              cursor: 'pointer',
            }}
          >
            {tenant.name}
          </button>
        ))}
      </div>
    </div>
  )
}

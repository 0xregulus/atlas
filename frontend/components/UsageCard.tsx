export function UsageCard({ title, value, caption }: { title: string; value: string; caption?: string }) {
  return (
    <div className="card">
      <p style={{ textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '0.1em', color: '#94a3b8' }}>{title}</p>
      <h2 style={{ fontSize: '2rem', margin: '0.2rem 0' }}>{value}</h2>
      {caption && <p style={{ color: '#94a3b8', margin: 0 }}>{caption}</p>}
    </div>
  )
}

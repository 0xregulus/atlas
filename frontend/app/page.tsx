'use client'

import { useCallback, useEffect, useState } from 'react'

import { UsageControls } from '@/components/UsageControls'
import { BillingCard } from '@/components/BillingCard'
import { TenantSwitcher } from '@/components/TenantSwitcher'
import { UsageCard } from '@/components/UsageCard'
import { ErrorBanner } from '@/components/ErrorBanner'
import { MetricsTimeline } from '@/components/MetricsTimeline'
import { ObservabilityPanel } from '@/components/ObservabilityPanel'
import { fetchTenantUsage, fetchUsageSummary, type TenantDataset, type TenantUsage, type UsageSummary } from '@/lib/api'

const observabilityPanelUrl = process.env.NEXT_PUBLIC_OBSERVABILITY_PANEL_URL

export default function Page() {
  const [tenant, setTenant] = useState('demo')
  const [usage, setUsage] = useState<TenantUsage | null>(null)
  const [loading, setLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [metrics, setMetrics] = useState<UsageSummary[] | null>(null)
  const [metricsError, setMetricsError] = useState<string | null>(null)

  const loadUsage = useCallback(
    async (targetTenant: string) => {
      try {
        setLoading(true)
        const data = await fetchTenantUsage(targetTenant)
        setUsage(data)
        setErrorMessage(null)
      } catch (err) {
        setErrorMessage('Unable to load tenant usage. Check API connectivity.')
      } finally {
        setLoading(false)
      }
    },
    []
  )

  const fetchMetrics = useCallback(async () => {
    try {
      setMetricsError(null)
      const summary = await fetchUsageSummary()
      setMetrics(summary)
    } catch (err) {
      setMetricsError('Metrics endpoint unavailable or missing CORE_API_BEARER_TOKEN.')
    }
  }, [])

  useEffect(() => {
    loadUsage(tenant)
  }, [tenant, loadUsage])

  useEffect(() => {
    fetchMetrics()
  }, [fetchMetrics])

  const handleRefresh = useCallback(async () => {
    await loadUsage(tenant)
  }, [loadUsage, tenant])

  return (
    <main>
      <header>
        <p style={{ color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.2em' }}>Atlas Control Plane</p>
        <h1 style={{ fontSize: '3rem', margin: '0.2rem 0' }}>AI Native Product Platform</h1>
        <p style={{ color: '#94a3b8' }}>Track multi-tenant usage, AI automations, and cost guardrails in one view.</p>
      </header>

      {errorMessage && <ErrorBanner message={errorMessage} onDismiss={() => setErrorMessage(null)} />}

      <TenantSwitcher activeTenant={tenant} onChange={(active) => setTenant(active)} />

      {loading && <p>Loading usage for {tenant}…</p>}

      {usage && (
        <>
          <section className="grid">
            <UsageCard title="Tokens" value={usage.usage.tokens.toLocaleString()} caption="30 day consumption" />
            <UsageCard title="Requests" value={usage.usage.requests.toLocaleString()} caption="Automation calls" />
            <UsageCard
              title="Plan"
              value={usage.usage.plan.toUpperCase()}
              caption={`Updated ${new Date(usage.refreshed_at).toLocaleTimeString()}`}
            />
            <BillingCard billing={usage.billing} />
          </section>

          <UsageControls
            tenant={tenant}
            onRefresh={handleRefresh}
            onError={(message) => setErrorMessage(message)}
          />
          <MetricsTimeline data={metrics} error={metricsError} onRetry={fetchMetrics} />
          <DatasetsPanel datasets={usage.datasets} tenant={tenant} />
          <ObservabilityPanel embedUrl={observabilityPanelUrl} />
        </>
      )}
    </main>
  )
}

function DatasetsPanel({ datasets, tenant }: { datasets?: TenantDataset[]; tenant: string }) {
  const items = datasets ?? defaultDatasets
  return (
    <div className="card">
      <h3>AI Knowledge Assets</h3>
      <p style={{ color: '#94a3b8' }}>Contracts shared with the LangGraph layer.</p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {items.map((dataset) => (
          <div key={`${tenant}-${dataset.name}`} style={{ display: 'flex', justifyContent: 'space-between' }}>
            <div>
              <span style={{ marginRight: '0.5rem' }}>{getDatasetIcon(dataset.name)}</span>
              <strong>{dataset.name}</strong>
              <span style={{ color: '#94a3b8', marginLeft: '0.5rem' }}>{dataset.description}</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ ...badgeStyle, background: freshnessColor(dataset.freshness) }}>
                Refreshed {dataset.freshness} ago
              </span>
              <a href={datasetDocLink(dataset.name)} style={{ color: '#60a5fa', textDecoration: 'none' }}>
                View docs ↗
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

const badgeStyle: React.CSSProperties = {
  borderRadius: '999px',
  padding: '0.2rem 0.75rem',
  fontSize: '0.75rem',
  color: '#0f172a',
  fontWeight: 600,
}

function freshnessColor(freshness: string): string {
  const value = parseInt(freshness, 10)
  if (Number.isNaN(value)) return '#fcd34d'
  if (freshness.includes('m') && value <= 30) return '#34d399'
  if (freshness.includes('h') && value <= 2) return '#fbbf24'
  return '#f87171'
}

function getDatasetIcon(name: string): string {
  switch (name) {
    case 'knowledge_base':
      return '📚'
    case 'sales_notes':
      return '📝'
    default:
      return '🗂️'
  }
}

const repoBase = 'https://github.com/your-org/atlas/blob/main'

function datasetDocLink(name: string): string {
  switch (name) {
    case 'knowledge_base':
      return `${repoBase}/data/transformations/models/staging/stg_knowledge_base.sql`
    case 'sales_notes':
      return `${repoBase}/data/transformations/models/marts/fct_ai_context.sql`
    default:
      return `${repoBase}/data`
  }
}

const defaultDatasets: TenantDataset[] = [
  { name: 'knowledge_base', description: 'Approved articles', freshness: '15m' },
  { name: 'sales_notes', description: 'Synced from CRM', freshness: '1h' },
]

const coreApiBase = process.env.NEXT_PUBLIC_CORE_API_URL || 'http://localhost:8000'

export type TenantUsage = {
  tenant: string
  usage: {
    tokens: number
    requests: number
    plan: string
  }
  refreshed_at: string
  datasets?: TenantDataset[]
  billing?: BillingPreview
}

export type TenantDataset = {
  name: string
  description: string
  freshness: string
}

export type BillingPreview = {
  tenant: string
  plan: string
  estimated_amount_usd: number
  next_charge_date: string
}

export type UsageSummary = {
  tenant: string
  events: number
  tokens: number
  latency_ms: number
  window_hours: number
}

export async function fetchTenantUsage(tenant?: string): Promise<TenantUsage> {
  const targetTenant = tenant || 'demo'

  try {
    const headers = { 'X-Atlas-Tenant': targetTenant }
    const [usageRes, catalogRes, billingRes] = await Promise.all([
      fetch(`${coreApiBase}/tenants/current`, { cache: 'no-store', headers }),
      fetch(`${coreApiBase}/tenants/${targetTenant}/catalog`, { cache: 'no-store', headers }),
      fetch(`${coreApiBase}/billing/${targetTenant}/preview`, { cache: 'no-store' }),
    ])

    if (!usageRes.ok) {
      throw new Error('Failed to fetch tenant usage')
    }

    const usagePayload = await usageRes.json()
    const catalog = catalogRes.ok ? await catalogRes.json() : null
    const billing = billingRes.ok ? await billingRes.json() : null

    return {
      tenant: usagePayload.tenant,
      usage: usagePayload.usage,
      refreshed_at: usagePayload.refreshed_at,
      datasets: catalog?.datasets,
      billing,
    }
  } catch (err) {
    console.warn('Falling back to mock usage', err)
    return {
      tenant: targetTenant,
      usage: { tokens: 0, requests: 0, plan: 'trial' },
      refreshed_at: new Date().toISOString(),
    }
  }
}

export async function fetchUsageSummary(): Promise<UsageSummary[] | null> {
  try {
    const res = await fetch('/api/metrics/usage', { cache: 'no-store' })
    if (res.status === 204) {
      return null
    }
    if (!res.ok) {
      const text = await res.text()
      throw new Error(text || 'Failed to fetch usage metrics')
    }
    return (await res.json()) as UsageSummary[]
  } catch (err) {
    console.warn('Unable to load usage summary', err)
    throw err
  }
}

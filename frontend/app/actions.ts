'use server'

import { revalidatePath } from 'next/cache'

const coreApiBase = process.env.CORE_API_URL || process.env.NEXT_PUBLIC_CORE_API_URL || 'http://localhost:8000'

const bearerToken = process.env.CORE_API_BEARER_TOKEN

async function atlasFetch(path: string, init?: RequestInit) {
  const res = await fetch(`${coreApiBase}${path}`, {
    cache: 'no-store',
    headers: {
      'Content-Type': 'application/json',
      ...(bearerToken ? { Authorization: `Bearer ${bearerToken}` } : {}),
      ...init?.headers,
    },
    ...init,
  })

  if (!res.ok) {
    const details = await res.text()
    throw new Error(`Atlas API error (${res.status}): ${details}`)
  }

  return res.json().catch(() => undefined)
}

export async function simulateUsage(tenant: string) {
  await atlasFetch('/tenants', {
    method: 'POST',
    body: JSON.stringify({ tenant, plan: 'growth' }),
  })

  const tokensDelta = Math.floor(Math.random() * 10_000)
  const requestsDelta = Math.floor(Math.random() * 200)

  await atlasFetch(`/tenants/${tenant}/usage`, {
    method: 'POST',
    body: JSON.stringify({ tokens_delta: tokensDelta, requests_delta: requestsDelta }),
  })

  revalidatePath('/')
  return { tokensDelta, requestsDelta }
}

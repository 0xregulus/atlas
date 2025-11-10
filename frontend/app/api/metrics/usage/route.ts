import { NextResponse } from 'next/server'

const coreApiBase = process.env.CORE_API_URL || process.env.NEXT_PUBLIC_CORE_API_URL || 'http://localhost:8000'
const bearerToken = process.env.CORE_API_BEARER_TOKEN

export async function GET() {
  if (!bearerToken) {
    return new NextResponse(null, { status: 204 })
  }

  try {
    const res = await fetch(`${coreApiBase}/metrics/usage/daily`, {
      headers: {
        Authorization: `Bearer ${bearerToken}`,
      },
      cache: 'no-store',
    })

    if (!res.ok) {
      const text = await res.text()
      return new NextResponse(text || 'Failed to fetch usage metrics', { status: res.status })
    }

    const payload = await res.json()
    return NextResponse.json(payload)
  } catch (err) {
    return new NextResponse('Metrics service unavailable', { status: 502 })
  }
}

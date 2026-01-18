import { NextResponse } from 'next/server'

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:5000'

export async function GET() {
  try {
    const res = await fetch(`${API_BASE}/api/project/info`, {
      cache: 'no-store',
    })
    if (!res.ok) {
      const error = await res.json()
      return NextResponse.json(error, { status: res.status })
    }
    const data = await res.json()
    return NextResponse.json(data)
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}

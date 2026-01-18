import { NextRequest, NextResponse } from 'next/server'

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:5000'

export async function GET() {
  try {
    const res = await fetch(`${API_BASE}/api/project/state`, {
      cache: 'no-store',
    })
    const data = await res.json()
    return NextResponse.json(data)
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const res = await fetch(`${API_BASE}/api/project/state`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    const data = await res.json()
    return NextResponse.json(data)
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}

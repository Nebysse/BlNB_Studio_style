import { NextRequest, NextResponse } from 'next/server'

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:5000'

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const path = searchParams.get('path') || ''
    const url = `${API_BASE}/api/files/list${path ? `?path=${encodeURIComponent(path)}` : ''}`
    
    const res = await fetch(url, {
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

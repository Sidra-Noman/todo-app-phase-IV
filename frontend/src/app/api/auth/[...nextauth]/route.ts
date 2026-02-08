// Minimal API route to avoid NextAuth App Router integration issues during build
import { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  // Return a simple response for auth API routes
  return NextResponse.json({ error: 'Auth not implemented in build' }, { status: 501 });
}

export async function POST(request: NextRequest) {
  // Return a simple response for auth API routes
  return NextResponse.json({ error: 'Auth not implemented in build' }, { status: 501 });
}
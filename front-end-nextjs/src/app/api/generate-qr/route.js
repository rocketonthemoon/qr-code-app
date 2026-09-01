// app/api/generate-qr/route.js
import { NextResponse } from 'next/server';
import axios from 'axios';

export async function POST(request) {
    try {
        const { searchParams } = new URL(request.url);
        const targetUrl = searchParams.get('url');

        if (!targetUrl) {
            return NextResponse.json({ error: 'URL query parameter is required' }, { status: 400 });
        }

        // INTERNAL_API_URL is populated on the server side (e.g. http://[FQDN of api in service connect namespace]:8000)
        const backendUrl = process.env.INTERNAL_API_URL || 'http://localhost:8000';

        const response = await axios.post(`${backendUrl}/api/generate-qr/?url=${encodeURIComponent(targetUrl)}`);

        return NextResponse.json(response.data);
    } catch (error) {
        console.error('Backend proxy error:', error.response?.data || error.message);
        const status = error.response?.status || 500;
        const message = error.response?.data || { error: 'Failed to generate QR code' };
        return NextResponse.json(message, { status });
    }
}
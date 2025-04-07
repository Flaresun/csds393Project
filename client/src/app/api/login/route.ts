import type { NextApiRequest, NextApiResponse } from 'next'
import { type NextRequest } from 'next/server'
import { headers } from 'next/headers'

export async function POST(req : Request) {
    const {email, password} = await req.json();

    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    return await fetch(process.env.BACKEND_URL + "/token",{
        method : "POST",
        body: formData,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            
        },
        credentials: 'include',
        
    }); 


}
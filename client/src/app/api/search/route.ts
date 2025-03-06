import type { NextApiRequest, NextApiResponse } from 'next'
import { type NextRequest } from 'next/server'
import { headers } from 'next/headers'



export async function POST(req : Request) {
    const {className} = await req.json();

    const res = await fetch(process.env.BACKEND_URL + "/get_class",{
        method : "POST",
        body: JSON.stringify({ class_name:className}),
        headers: {
            'Content-Type': 'application/json',
        }
    }); 
    const data = await res.json();
    console.log(data)
    return Response.json({ data });

}
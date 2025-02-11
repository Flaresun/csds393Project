import type { NextApiRequest, NextApiResponse } from 'next'
import { type NextRequest } from 'next/server'
import { headers } from 'next/headers'

type ResponseData = {
    success : boolean,
    message: string
  }

export async function POST(req : Request) {
    const {email, password} = await req.json();

    const res = await fetch(process.env.BACKEND_URL + "/login",{
        method : "POST",
        body: JSON.stringify({ email:email, password:password }),
        headers: {
            'Content-Type': 'application/json',
        }
    }); 
    const data = await res.json();
    console.log(data)
    return Response.json({ data });

}
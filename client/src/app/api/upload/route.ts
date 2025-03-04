import type { NextApiRequest, NextApiResponse } from 'next'
import { type NextRequest } from 'next/server'
import { headers } from 'next/headers'
type ResponseData = {
    success : boolean,
    message: string
  }
export async function POST(req : Request) {
    const formData = await req.formData();
    const res = await fetch(process.env.BACKEND_URL + "/upload",{
        method : "POST",
        body:formData,
        headers: {
        }
    }); 
    const data = await res.json();
    return Response.json({ data });
}

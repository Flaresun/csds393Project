import type { NextApiRequest, NextApiResponse } from 'next'
import { type NextRequest } from 'next/server'
import { headers } from 'next/headers'

type ResponseData = {
    success : boolean,
    message: string
  }

export async function POST(req : Request) {
    const {email, password, role} = await req.json();
    
<<<<<<< HEAD
    return await fetch(process.env.BACKEND_URL + "/sign_up",{
=======
    return await fetch(process.env.BACKEND_URL + "/signup",{
>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8
        method : "POST",
        body: JSON.stringify({ email:email, password:password, role:role }),
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
    }); 

}
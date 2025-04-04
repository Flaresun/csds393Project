import type { NextApiRequest, NextApiResponse } from 'next'
import { type NextRequest } from 'next/server'
import { headers } from 'next/headers'

export async function POST(req : Request) {
    const {email, password} = await req.json();

<<<<<<< HEAD
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    return await fetch(process.env.BACKEND_URL + "/token",{
=======
    return await fetch(process.env.BACKEND_URL + "/login",{
>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8
        method : "POST",
        body: formData,
        headers: {
<<<<<<< HEAD
            'Content-Type': 'application/x-www-form-urlencoded',
=======
            'Content-Type': 'application/json',
>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8
            
        },
        credentials: 'include',
        
    }); 


}
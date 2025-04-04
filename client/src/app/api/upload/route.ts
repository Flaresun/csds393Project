<<<<<<< HEAD
export async function POST(req : Request) {
    const formData = await req.formData();
    const sectionId = formData.get("sectionId");
    const token = formData.get('token');
    formData.append("section_id", sectionId)

    
    const res = await fetch(process.env.BACKEND_URL + "/upload_note",{
        method : "POST",
        body:formData,
        headers: {Authorization: `Bearer ${token}`,},
=======
import type { NextApiRequest, NextApiResponse } from 'next'
import { type NextRequest } from 'next/server'
import { headers } from 'next/headers'
type ResponseData = {
    success : boolean,
    message: string
  }
export async function POST(req : Request) {
    const formData = await req.formData();
    const className = formData.get("className");
    const userEmail = formData.get("email");

    formData.append("className", className)
    formData.append("email", userEmail)
    console.log(className, userEmail)
    const res = await fetch(process.env.BACKEND_URL + "/upload",{
        method : "POST",
        body:formData,
        headers: {
        },
>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8
        credentials: "include",
    }); 
    const data = await res.json();
    return Response.json({ data });
<<<<<<< HEAD
}
=======
}
>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8

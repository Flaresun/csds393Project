import type { NextApiRequest, NextApiResponse } from 'next'
import { type NextRequest } from 'next/server'
import { headers } from 'next/headers'

type ResponseData = {
    success: boolean;
    message: string;
};

export async function POST(req: Request) {
    // Extract email, password, and role from the incoming JSON request body
    const { email, password, role } = await req.json();

    // Send a POST request to the backend API to handle the sign-up process
    const res = await fetch(process.env.BACKEND_URL + "/sign_up", {
        method: "POST", // HTTP method for the request
        body: JSON.stringify({ email, password, role }), // Request body containing user data (email, password, role)
        headers: {
            'Content-Type': 'application/json', // Ensure the content type is JSON
        },
        credentials: 'include', // Ensure credentials (cookies) are included in the request for session handling
    });

    // Return the response received from the backend (this can be a success/failure message)
    return res;
}

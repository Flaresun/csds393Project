import type { NextApiRequest, NextApiResponse } from 'next'
import { type NextRequest } from 'next/server'
import { headers } from 'next/headers'

/**
 * Handles the POST request for logging in a user by sending the user's credentials 
 * (email and password) to the backend to obtain an authentication token.
 *
 * This function expects the request body to be in JSON format with the following fields:
 * - `email`: The user's email address (username).
 * - `password`: The user's password.
 * 
 * The function then constructs a form data payload, sending the credentials in the 
 * `application/x-www-form-urlencoded` format to the backend's `/token` endpoint.
 * 
 * @param req - The incoming HTTP request.
 * @returns The response from the backend after attempting to authenticate the user.
 */
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

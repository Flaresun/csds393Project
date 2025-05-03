export async function POST(req: Request) {
    // Extract the 'token' from the incoming request body (JSON format)
    const { token } = await req.json();

    // Make a POST request to the backend URL for user validation
    return await fetch(process.env.BACKEND_URL + "/validate_user", {
        method: "POST", // HTTP method for the request
        headers: {
            'Content-Type': 'application/json', // Specify the content type of the request body
            Authorization: `Bearer ${token}`, // Add the 'Authorization' header with the token as a Bearer token
        },
        credentials: "include", // Ensure credentials (cookies) are included with the request
    });
}

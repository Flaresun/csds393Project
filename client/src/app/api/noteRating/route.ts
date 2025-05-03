export async function POST(req: Request) {
    // Extract note_id, rating, and token from the incoming JSON request body
    const { note_id, rating, token } = await req.json();

    // Send a POST request to the backend API to rate the note
    const res = await fetch(process.env.BACKEND_URL + "/rate_note", {
        method: "POST", // HTTP method for the request
        body: JSON.stringify({ note_id, rating }), // Request body containing the note ID and rating
        headers: {
            'Content-Type': 'application/json', // Ensure the content type is JSON
            Authorization: `Bearer ${token}`, // Include the token for authentication
        },
        credentials: 'include', // Ensure credentials (cookies) are included in the request for session handling
    });

    // Return the response from the backend (this can include a success or failure message)
    return res;
}

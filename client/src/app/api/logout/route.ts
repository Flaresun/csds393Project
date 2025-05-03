export async function POST(req: Request) {
    // Send a POST request to the backend API to log out the user
    const res = await fetch(process.env.BACKEND_URL + "/logout", {
        method: "POST", // HTTP method for the request
        headers: {
            'Content-Type': 'application/json', // Indicate that the content being sent is JSON
        },
        credentials: 'include', // Include credentials (cookies) in the request for session management
    });

    // Return the response from the backend API (could be success or failure of the logout action)
    return res;
}

export async function POST(req: Request) {
    // Extract form data from the incoming request
    const formData = await req.formData();

    // Retrieve 'sectionId' and 'token' from the form data
    const sectionId = formData.get("sectionId");
    const token = formData.get('token');
    
    // Append 'section_id' to the form data with the value from 'sectionId'
    formData.append("section_id", sectionId);

    // Log the values for debugging purposes (sectionId and token)
    console.log(sectionId);
    console.log(token);

    // Make a POST request to the backend API to upload the note
    const res = await fetch(process.env.BACKEND_URL + "/upload_note", {
        method: "POST", // HTTP method for the request
        body: formData, // Form data sent as the body of the request
        headers: {
            Authorization: `Bearer ${token}`, // Authorization header with Bearer token for authentication
        },
        credentials: "include", // Ensure credentials (cookies) are included with the request
    });

    // Parse the JSON response from the backend
    const data = await res.json();

    // Return the response data as JSON
    return Response.json({ data });
}

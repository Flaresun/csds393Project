
/**
 * Handles the POST request to fetch the role associated with a given email.
 *
 * This function expects the request body to contain the following field:
 * - `email`: The email address for which the role needs to be retrieved.
 * 
 * The function sends the email to the backend endpoint `/get_role_given_email` 
 * in a POST request to retrieve the role associated with the given email.
 * 
 * @param req - The incoming HTTP request containing the email.
 * @returns The response from the backend containing the role information for the given email.
 */
export async function POST(req : Request) {    
    const {email} = await req.json();

    return await fetch(process.env.BACKEND_URL + "/get_role_given_email",{
        method : "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email}),
    }); 
}

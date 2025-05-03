/**
 * Handles the POST request to fetch comments for a specific note.
 *
 * This function sends a POST request to the backend endpoint `/get_comments_for_note`
 * with the note ID to retrieve all comments associated with that note. The request
 * includes an authorization token for secure access.
 *
 * @param req - The incoming HTTP request containing the note ID and token.
 * @returns The response from the backend containing the comments for the specified note.
 */
export async function POST(req : Request) {
    const {note_id,token} = await req.json();
    
    return await fetch(process.env.BACKEND_URL + "/get_comments_for_note",{
        method : "POST",
        body: JSON.stringify({ note_id:note_id}),
        headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`,},
        credentials: 'include',
    }); 
}

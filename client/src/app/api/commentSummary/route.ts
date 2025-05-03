/**
 * Handles the POST request to fetch a comment summary for a given note.
 *
 * This function sends a POST request to the backend endpoint `/get_comment_summary`
 * with the note ID to retrieve the summary of comments related to the note.
 *
 * @param req - The incoming HTTP request containing the note ID for which the comment summary is requested.
 * @returns The response from the backend containing the comment summary for the specified note.
 */
export async function POST(req : Request) {    
    const {note_id} = await req.json();

    return await fetch(process.env.BACKEND_URL + "/get_comment_summary",{
        method : "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({note_id : note_id}),
    }); 
}

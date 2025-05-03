/**
 * Handles the POST request to delete a note.
 *
 * This function sends a POST request to the backend endpoint `/delete_note`
 * with the note ID to delete the specified note. The request includes an authorization
 * token for secure access.
 *
 * @param req - The incoming HTTP request containing the note ID and token.
 * @returns The response from the backend indicating the success or failure of the note deletion.
 */
export async function POST(req : Request) {    
    const {note_id, token} = await req.json();

    return await fetch(process.env.BACKEND_URL + "/delete_note",{
        method : "POST",
        headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`,},
        body: JSON.stringify({note_id}),
    }); 
}

/**
 * Handles the POST request to leave a comment on a note.
 *
 * This function sends a POST request to the backend endpoint `/leave_comment`
 * with the provided note ID, parent comment ID (if any), and the comment content.
 * The comment will be associated with the specified note.
 *
 * @param req - The incoming HTTP request containing the note ID, parent comment ID (if applicable), content of the comment, and the authentication token.
 * @returns The response from the backend, typically confirming the successful submission of the comment.
 */
export async function POST(req : Request) {
    const {note_id, parent_id, content, token} = await req.json();
    
    return await fetch(process.env.BACKEND_URL + "/leave_comment",{
        method : "POST",
        body: JSON.stringify({ note_id:note_id, parent_com_id:null, content:content }),
        headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`,},
        credentials: 'include',
    }); 
}


export async function POST(req : Request) {
    const {note_id,token} = await req.json();
    
    return await fetch(process.env.BACKEND_URL + "/get_comments_for_note",{
        method : "POST",
        body: JSON.stringify({ note_id:note_id}),
        headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`,},
        credentials: 'include',
    }); 

}
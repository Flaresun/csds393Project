
export async function POST(req : Request) {    
    const {note_id, token} = await req.json();

    return await fetch(process.env.BACKEND_URL + "/delete_note",{
        method : "POST",
        headers: {'Content-Type': 'application/json',Authorization: `Bearer ${token}`,},
        body: JSON.stringify({note_id}),
    }); 

}
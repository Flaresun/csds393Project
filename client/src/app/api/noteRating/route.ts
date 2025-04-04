
export async function POST(req : Request) {
    const {note_id, rating,token} = await req.json();
    
    return await fetch(process.env.BACKEND_URL + "/rate_note",{
        method : "POST",
        body: JSON.stringify({ note_id:note_id,rating :rating }),
        headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`,},
        credentials: 'include',
    }); 

}
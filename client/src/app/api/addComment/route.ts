
export async function POST(req : Request) {
    const {note_id, parent_id, content,token} = await req.json();
    
    return await fetch(process.env.BACKEND_URL + "/leave_comment",{
        method : "POST",
        body: JSON.stringify({ note_id:note_id, parent_com_id:null, content:content }),
        headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`,},
        credentials: 'include',
    }); 

}
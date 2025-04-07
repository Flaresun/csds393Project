export async function POST(req : Request) {
    const formData = await req.formData();
    const sectionId = formData.get("sectionId");
    const token = formData.get('token');
    formData.append("section_id", sectionId)

    
    const res = await fetch(process.env.BACKEND_URL + "/upload_note",{
        method : "POST",
        body:formData,
        headers: {Authorization: `Bearer ${token}`,},
        credentials: "include",
    }); 
    const data = await res.json();
    return Response.json({ data });
}

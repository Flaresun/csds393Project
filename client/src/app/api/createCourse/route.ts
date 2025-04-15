
export async function POST(req : Request) {
    const {departmentCode,courseCode, name,token} = await req.json();
    
    return await fetch(process.env.BACKEND_URL + "/create_course",{
        method : "POST",
        body: JSON.stringify({ department:departmentCode, code:courseCode, name:name}),
        headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`,},
        credentials: 'include',
    }); 

}
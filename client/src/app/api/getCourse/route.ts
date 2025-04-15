
export async function POST(req : Request) {    
    const {department} = await req.json();

    return await fetch(process.env.BACKEND_URL + "/get_courses",{
        method : "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ department:department}),
    }); 

}
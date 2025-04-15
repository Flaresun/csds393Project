
export async function POST(req : Request) {    
    const {department, course} = await req.json();

    return await fetch(process.env.BACKEND_URL + "/get_sections",{
        method : "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ department:department, course:course}),
    }); 

}
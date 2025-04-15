
export async function GET(req : Request) {    
    return await fetch(process.env.BACKEND_URL + "/get_departments",{
        method : "GET",
        headers: {'Content-Type': 'application/json'},
    }); 

}
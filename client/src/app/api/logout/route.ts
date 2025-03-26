export async function POST(req : Request) {
    return await fetch(process.env.BACKEND_URL + "/logout",{
        method : "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: "include"
    }); 


}
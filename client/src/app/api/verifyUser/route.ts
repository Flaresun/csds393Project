export async function POST(req : Request) {
    const {token} = await req.json();

    return await fetch(process.env.BACKEND_URL + "/validate_user",{
        method : "POST",
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
        },
        credentials: "include"
    }); 


}
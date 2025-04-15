
export async function POST(req : Request) {
    const {departmentCode,courseCode,email,year,semester,token} = await req.json();
    
    return await fetch(process.env.BACKEND_URL + "/create_section",{
        method : "POST",
        body: JSON.stringify({ department:departmentCode, course:courseCode, instructor:email, year:year, semester:semester}),
        headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`,},
        credentials: 'include',
    }); 

}
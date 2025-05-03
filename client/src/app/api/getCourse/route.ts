/**
 * Handles the POST request to fetch courses for a specific department.
 *
 * This function sends a POST request to the backend endpoint `/get_courses`
 * with the department information to retrieve the courses related to that department.
 *
 * @param req - The incoming HTTP request containing the department information.
 * @returns The response from the backend containing the list of courses for the specified department.
 */
export async function POST(req : Request) {    
    const {department} = await req.json();

    return await fetch(process.env.BACKEND_URL + "/get_courses",{
        method : "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ department:department}),
    }); 
}

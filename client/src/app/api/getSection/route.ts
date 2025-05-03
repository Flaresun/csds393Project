/**
 * Handles the POST request to fetch sections for a specific department and course.
 *
 * This function expects the request body to contain the following fields:
 * - `department`: The department code (e.g., 'CS', 'MATH').
 * - `course`: The course code (e.g., '101', '202').
 * 
 * The function sends these details in a POST request to the backend endpoint `/get_sections` 
 * to retrieve the relevant sections for the specified department and course.
 * 
 * @param req - The incoming HTTP request containing the department and course information.
 * @returns The response from the backend with the list of sections for the given course and department.
 */
export async function POST(req : Request) {    
    const {department, course} = await req.json();

    return await fetch(process.env.BACKEND_URL + "/get_sections",{
        method : "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ department:department, course:course}),
    }); 
}

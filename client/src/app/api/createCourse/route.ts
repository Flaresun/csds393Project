/**
 * Handles the POST request to create a new course.
 *
 * This function sends a POST request to the backend endpoint `/create_course`
 * with the department code, course code, and course name. It also includes an
 * authorization token for secure access to the backend.
 *
 * @param req - The incoming HTTP request containing the necessary data to create a course.
 * @returns The response from the backend indicating the success or failure of the course creation.
 */
export async function POST(req : Request) {
    const {departmentCode, courseCode, name, token} = await req.json();
    
    return await fetch(process.env.BACKEND_URL + "/create_course",{
        method : "POST",
        body: JSON.stringify({ department: departmentCode, code: courseCode, name: name }),
        headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`,},
        credentials: 'include',
    }); 
}

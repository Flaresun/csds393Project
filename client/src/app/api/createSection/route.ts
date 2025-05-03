/**
 * Handles the POST request to create a new section for a course.
 *
 * This function sends a POST request to the backend endpoint `/create_section`
 * with the department code, course code, instructor's email, year, and semester.
 * It also includes an authorization token for secure access to the backend.
 *
 * @param req - The incoming HTTP request containing the necessary data to create a section.
 * @returns The response from the backend indicating the success or failure of the section creation.
 */
export async function POST(req : Request) {
    const {departmentCode, courseCode, email, year, semester, token} = await req.json();
    
    return await fetch(process.env.BACKEND_URL + "/create_section",{
        method : "POST",
        body: JSON.stringify({ department: departmentCode, course: courseCode, instructor: email, year: year, semester: semester }),
        headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`,},
        credentials: 'include',
    }); 
}

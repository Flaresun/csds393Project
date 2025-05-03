/**
 * Handles the GET request to fetch the list of departments.
 *
 * This function sends a GET request to the backend endpoint `/get_departments`
 * to retrieve the available departments.
 * 
 * @param req - The incoming HTTP request.
 * @returns The response from the backend containing the list of departments.
 */
export async function GET(req : Request) {    
    return await fetch(process.env.BACKEND_URL + "/get_departments",{
        method : "GET",
        headers: {'Content-Type': 'application/json'},
    }); 
}

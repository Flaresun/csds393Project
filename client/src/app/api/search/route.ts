import type { NextApiRequest, NextApiResponse } from 'next'
import { type NextRequest } from 'next/server'
import { headers } from 'next/headers'



export async function POST(req : Request) {
    const {className,token} = await req.json();
    const allData = []
    
    const res =  await fetch(process.env.BACKEND_URL + "/get_courses",{
        method : "POST",
        body: JSON.stringify({ department:className}),
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
        },
        credentials: "include"
    }); 

    const {data} = await res.json()
    console.log(data.courses)
    // For each course, get the department name and course name. 
    // Then using those, get the section id 
    // Then using the section id, get the note
    // Package them (course name, note content, ...)
    
    for (let i = 0; i < data.courses.length; i++) {
        let dept_name = data.courses[i].split(" ")[0];


        const res =  await fetch(process.env.BACKEND_URL + "/get_sections",{
            method : "POST",
            body: JSON.stringify({ department:dept_name, course:data.courses[i]}),
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
            },
            credentials: "include"
        }); 

        const section= await res.json();
        const sections = section.data
        console.log(sections)
        

        for (let j = 0; j < sections.sections.length; j++) {
            let sectionId = sections.sections[j].id;
            let instructor = sections.sections[j].instructor;
            let year = sections.sections[j].year;
            let semester = sections.sections[j].semester;
            

            const res =  await fetch(process.env.BACKEND_URL + "/get_notes_for_section",{
                method : "POST",
                body: JSON.stringify({ section_id:sectionId, ids_only:false}),
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                credentials: "include"
            });

            const noteData = await res.json();

            for (let k = 0; k < noteData.notes.length; k++) {
                let currentNoteId = noteData.notes[k].id;
                console.log(currentNoteId)
                allData.push({
                    id: currentNoteId,
                    name: data.courses[i],
                    instructor: instructor,
                    year: year,
                    semester: semester,
                    content: noteData.notes[k].content
                })
            }

            
        }
    }

    //return res
    return Response.json({allData})

}
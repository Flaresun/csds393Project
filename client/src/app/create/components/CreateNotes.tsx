// components/CourseManager.tsx
'use client';

import { useState } from 'react';



type Course = {
  departmentCode: string;
  courseCode: string;
  courseName: string;
};

type Section = {
  departmentCode: string;
  courseCode: string;
  instructorEmail: string;
  year: string;
  semester: string;
};

export default function CourseManager() {

    const token = document.cookie
    .split("; ")
    .find(row => row.startsWith("token="))?.split("=")[1];

    if (!token) {
        console.error("No token found");
        return;
    }

    const [course, setCourse] = useState<Course>({
        departmentCode: '',
        courseCode: '',
        courseName: '',
    });

    const [section, setSection] = useState<Section>({
        departmentCode: '',
        courseCode: '',
        instructorEmail: '',
        year: '',
        semester: '',
    });

    const handleCourseChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setCourse({ ...course, [e.target.name]: e.target.value });
    };

    const handleSectionChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setSection({ ...section, [e.target.name]: e.target.value });
    };

    const handleCreateCourse = async () => {
        const res = await fetch("/api/createCourse", {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
            },
            credentials: "include",
            body: JSON.stringify({ departmentCode : course.departmentCode, courseCode : course.courseCode, name: course.courseName,token:token}),
        });
    
        const data = await res.json();
        console.log(data);
    };

    const handleAddSection = async () => {
        const res = await fetch("/api/createSection", {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
            },
            credentials: "include",
            body: JSON.stringify({ departmentCode : section.departmentCode.toUpperCase(), courseCode : section.courseCode.toUpperCase(), email: section.instructorEmail, year: section.year, semester: section.semester,token:token}),
        });
    
        const data = await res.json();
        console.log(data);
    };

    return (
        <div className="max-w-2xl mx-auto p-6 space-y-8 text-slate-900">
        <div className="bg-white shadow-md rounded-xl p-6">
            <h2 className="text-xl font-semibold mb-4">Create Course</h2>
            <div className="space-y-4">
            <input
                name="departmentCode"
                value={course.departmentCode}
                onChange={handleCourseChange}
                placeholder="Department Code"
                className="w-full p-2 border rounded-md"
            />
            <input
                name="courseCode"
                value={course.courseCode}
                onChange={handleCourseChange}
                placeholder="Course Code"
                className="w-full p-2 border rounded-md"
            />
            <input
                name="courseName"
                value={course.courseName}
                onChange={handleCourseChange}
                placeholder="Course Name"
                className="w-full p-2 border rounded-md"
            />
            <button
                onClick={handleCreateCourse}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
            >
                Create Course
            </button>
            </div>
        </div>

        <div className="bg-white shadow-md rounded-xl p-6">
            <h2 className="text-xl font-semibold mb-4">Add Section</h2>
            <div className="space-y-4">
            <input
                name="departmentCode"
                value={section.departmentCode}
                onChange={handleSectionChange}
                placeholder="Department Code"
                className="w-full p-2 border rounded-md"
            />
            <input
                name="courseCode"
                value={section.courseCode}
                onChange={handleSectionChange}
                placeholder="Course Code"
                className="w-full p-2 border rounded-md"
            />
            <input
                name="instructorEmail"
                value={section.instructorEmail}
                onChange={handleSectionChange}
                placeholder="Instructor Email"
                className="w-full p-2 border rounded-md"
            />
            <input
                name="year"
                value={section.year}
                onChange={handleSectionChange}
                placeholder="Year"
                className="w-full p-2 border rounded-md"
            />
            <select
                name="semester"
                value={section.semester}
                onChange={handleSectionChange}
                className="w-full p-2 border rounded-md"
            >
                <option value="">Select Semester</option>
                <option value="Fall">Fall</option>
                <option value="Spring">Spring</option>
                <option value="Summer">Summer</option>
            </select>
            <button
                onClick={handleAddSection}
                className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
            >
                Add Section
            </button>
            </div>
        </div>
        </div>
    );
}

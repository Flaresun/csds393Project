'use client';

import { useState } from 'react';

// Define the types for Course and Section data
type Course = {
  departmentCode: string; // Department code for the course
  courseCode: string; // Course code
  courseName: string; // Course name
};

type Section = {
  departmentCode: string; // Department code for the section
  courseCode: string; // Course code for the section
  instructorEmail: string; // Email of the instructor for the section
  year: string; // Year the section is offered
  semester: string; // Semester (e.g., Fall, Spring, Summer)
};

export default function CourseManager() {
  // Retrieve the token from the document's cookies
  const token = document.cookie
    .split("; ")
    .find(row => row.startsWith("token="))?.split("=")[1];

  // If token is not found, log an error and return nothing
  if (!token) {
    console.error("No token found");
    return;
  }

  // State variables for course and section details
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

  // Handle changes in course input fields
  const handleCourseChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCourse({ ...course, [e.target.name]: e.target.value });
  };

  // Handle changes in section input fields
  const handleSectionChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setSection({ ...section, [e.target.name]: e.target.value });
  };

  // Handle course creation by making a POST request to the server
  const handleCreateCourse = async () => {
    const res = await fetch("/api/createCourse", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`, // Add token to Authorization header
      },
      credentials: "include", // Send credentials (cookies)
      body: JSON.stringify({ departmentCode: course.departmentCode, courseCode: course.courseCode, name: course.courseName, token }),
    });
    
    const data = await res.json(); // Parse response data
    console.log(data); // Log response
  };

  // Handle section addition by making a POST request to the server
  const handleAddSection = async () => {
    const res = await fetch("/api/createSection", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`, // Add token to Authorization header
      },
      credentials: "include", // Send credentials (cookies)
      body: JSON.stringify({
        departmentCode: section.departmentCode.toUpperCase(),
        courseCode: section.courseCode.toUpperCase(),
        email: section.instructorEmail,
        year: section.year,
        semester: section.semester,
        token,
      }),
    });

    const data = await res.json(); // Parse response data
    console.log(data); // Log response
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-8 text-slate-900 ">
      {/* Course Creation Form */}
      <div className="bg-slate-200 shadow-md rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4">Create Course</h2>
        <div className="space-y-4">
          <input
            name="departmentCode"
            value={course.departmentCode}
            onChange={handleCourseChange}
            placeholder="Department Code"
            className="w-full p-2 border rounded-md bg-slate-200"
          />
          <input
            name="courseCode"
            value={course.courseCode}
            onChange={handleCourseChange}
            placeholder="Course Code"
            className="w-full p-2 border rounded-md bg-slate-200"
          />
          <input
            name="courseName"
            value={course.courseName}
            onChange={handleCourseChange}
            placeholder="Course Name"
            className="w-full p-2 border rounded-md bg-slate-200"
          />
          <button
            onClick={handleCreateCourse}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Create Course
          </button>
        </div>
      </div>

      {/* Section Addition Form */}
      <div className="bg-slate-200 shadow-md rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4">Add Section</h2>
        <div className="space-y-4">
          <input
            name="departmentCode"
            value={section.departmentCode}
            onChange={handleSectionChange}
            placeholder="Department Code"
            className="w-full p-2 border rounded-md bg-slate-200"
          />
          <input
            name="courseCode"
            value={section.courseCode}
            onChange={handleSectionChange}
            placeholder="Course Code"
            className="w-full p-2 border rounded-md bg-slate-200"
          />
          <input
            name="instructorEmail"
            value={section.instructorEmail}
            onChange={handleSectionChange}
            placeholder="Instructor Email"
            className="w-full p-2 border rounded-md bg-slate-200"
          />
          <input
            name="year"
            value={section.year}
            onChange={handleSectionChange}
            placeholder="Year"
            className="w-full p-2 border rounded-md bg-slate-200"
          />
          <select
            name="semester"
            value={section.semester}
            onChange={handleSectionChange}
            className="w-full p-2 border rounded-md bg-slate-200"
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

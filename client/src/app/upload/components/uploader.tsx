"use client";
import React, { useEffect, useState } from "react";

// Type definition for Section
type Section = { id: number; instructor: string, semester: string, year: number};

const UploadPage = () => {
  const [departments, setDepartments] = useState<[]>([]);
  const [courses, setCourses] = useState<[]>([]);
  const [sections, setSections] = useState<Section[]>([]);

  const [selectedDepartment, setSelectedDepartment] = useState("");
  const [selectedCourse, setSelectedCourse] = useState("");
  const [selectedSection, setSelectedSection] = useState<string>();

  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const token = document?.cookie
    .split("; ")
    .find((row) => row.startsWith("token="))
    ?.split("=")[1];

  /**
   * Fetches departments from the API when the component mounts.
   * This function is triggered by the `useEffect` hook when the component first renders.
   */
  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const res = await fetch("/api/getDepartment", {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json',
            },
        });
        const {data} = await res.json();
        setDepartments(data.departments);
      } catch (error) {
        console.error("Error fetching departments:", error);
      }
    };
    fetchDepartments();
  }, []);

  /**
   * Fetches courses based on the selected department.
   * Triggered whenever `selectedDepartment` changes.
   */
  useEffect(() => {
    const fetchCourses = async () => {
      if (!selectedDepartment) return;
      try {
        const res = await fetch("/api/getCourse", {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ department : selectedDepartment}),
        });
        const {data} = await res.json();
        setCourses(data.courses);
        setSections([]);
        setSelectedCourse("");
        setSelectedSection("");
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    };
    fetchCourses();
  }, [selectedDepartment]);

  /**
   * Fetches sections based on the selected course and department.
   * Triggered whenever `selectedCourse` changes.
   */
  useEffect(() => {
    const fetchSections = async () => {
      if (!selectedCourse) return;
      try {
        const res = await fetch("/api/getSection", {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ department : selectedDepartment, course: selectedCourse}),
        });
        const {data} = await res.json();
        console.log(data.sections[0].id)
        setSections(data.sections);
        setSelectedSection(data.sections[0].id);
      } catch (error) {
        console.error("Error fetching sections:", error);
      }
    };
    fetchSections();
  }, [selectedCourse]);

  /**
   * Handles file input changes and updates the `file` state.
   * @param {React.ChangeEvent<HTMLInputElement>} event - The file input change event.
   */
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  /**
   * Uploads the selected file and related metadata (e.g., section ID) to the server.
   * Displays a success or error message based on the outcome.
   */
  const uploadFile = async () => {
    if (!file || !selectedSection) {
      setMessage("Please complete all selections and choose a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("sectionId", selectedSection);
    formData.append("token", token || "");

    try {
        const res = await fetch("/api/upload", {
            method: 'POST',
            headers: {
            Authorization: `Bearer ${token}`,
            },
            credentials: "include",
            body: formData,
        });
    
        const {data} = await res.json();
        setMessage(`File uploaded successfully! File ID: ${data.id}`);
    } catch (error) {
      console.error(error);
      setMessage("File upload failed.");
    }
  };

  return (
    <div className="min-h-screen bg-blue-950 flex items-center justify-center p-4 text-slate-900">
      <div className="bg-white text-slate-900 p-6 rounded-xl shadow-lg w-full max-w-md space-y-5">
        <h2 className="text-xl font-semibold text-center">Upload Notes</h2>

        {/* Department Dropdown */}
        <select
          value={selectedDepartment}
          onChange={(e) => setSelectedDepartment(e.target.value)}
          className="w-full p-2 border rounded"
        >
          <option value="">Select Department</option>
          {departments.map((dept, index) => (
            <option key={index} value={dept.name}>
              {dept}
            </option>
          ))}
        </select>

        {/* Course Dropdown */}
        <select
          value={selectedCourse}
          onChange={(e) => setSelectedCourse(e.target.value)}
          className="w-full p-2 border rounded"
          disabled={!selectedDepartment}
        >
          <option value="">Select Course</option>
          {courses.map((course, index) => (
            <option key={index} value={course}>
              {course}
            </option>
          ))}
        </select>

        {/* Section Dropdown */}
        <select
          value={selectedSection}
          onChange={(e) => setSelectedSection(e.target.value)}
          className="w-full p-2 border rounded"
          disabled={!selectedCourse}
        >
          <option value="">Select Section</option>
          {sections.map((section, index) => (
            <option key={index} value={section.id}>
              Instructor: {section.instructor}| 
              Semester: {section.semester}| 
              Year: {section.year}
            </option>
          ))}
        </select>

        {/* File Input */}
        <input type="file" accept=".pdf,.docx" onChange={handleFileChange} className="w-full" />

        {/* Upload Button */}
        <button
          onClick={uploadFile}
          className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Upload File
        </button>

        {/* Message */}
        {message && <p className="text-center text-gray-700">{message}</p>}
      </div>
    </div>
  );
};

export default UploadPage;

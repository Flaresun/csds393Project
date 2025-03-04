"use client";
import React from 'react'
import { useState } from "react";
import axios from "axios";
import './uploader.css';

const page = () => {
    
    const [file, setFile] = useState<File | null>(null);
    const [message, setMessage] = useState("");
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
        setFile(event.target.files[0]);
        }
    };
    const uploadFile = async () => {
        if (!file) {
            setMessage("Please select a file first.");
        return;
        }
        const formData = new FormData();
        formData.append("file", file);
        try {
        const {data} = await axios.post("api/upload", formData, {
            headers: { "Content-Type": "multipart/form-data" },
        });
        console.log(data);
        setMessage(`File uploaded successfully! File ID: ${data.file_id}`);
        } catch (error) {
        setMessage("File upload failed.");
        }
    };
    return (
        <div className="flex items-center justify-center w-full min-h-screen bg-gray-800">
            <div className="flex flex-wrap items-center justify-center p-6 max-w-md mx-auto rounded-xl shadow-md space-y-4 fileUploadForm">
                <span className="uploadText">Upload a File</span>
                <div className="flex flex-col sm:flex-row items-center w-full space-y-2 sm:space-y-0 sm:space-x-4">
                    <input type="file" accept=".pdf,.docx" onChange={handleFileChange} className='pl-20 pb-5 md:pl-0 pb-0 lg:pl-0 pb-0'/>
                    
                    <button
                        onClick={uploadFile}
                        className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
                    >
                        Upload
                    </button>
                    {message && <p className="text-center text-gray-700">{message}</p>}
                </div>
            </div>
        </div>
    );
};  
export default page

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
            <div className="flex items-center justify-center p-6 max-w-md mx-auto rounded-xl shadow-md space-y-4 fileUploadForm">
                <span className="uploadText">Upload an image</span>
                
                <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
                
                <button
                    onClick={uploadFile}
                    className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
                >
                    Upload
                </button>
                {message && <p className="text-center text-gray-700">{message}</p>}
            </div>
        </div>
    );
};  
export default page

"use client";
import React, { useContext } from 'react'
import { useState } from "react";
import axios from "axios";
import { AppContent } from '@/context/AppContext';
const page = () => {
    
    const [file, setFile] = useState<File | null>(null);
    const [message, setMessage] = useState("");
    const [className, setClassName] = useState("");
    const {userEmail} = useContext(AppContent)

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
        formData.append("className", className);
        formData.append("email",userEmail)
        console.log(userEmail)
        try {
            const {data} = await axios.post("api/upload",formData, {
                headers: { "Content-Type": "multipart/form-data"},
            });
            console.log(data);
            setMessage(`File uploaded successfully! File ID: ${data.file_id}`);
        } catch (error) {
            setMessage("File upload failed.");
        }
    };
    
    return (
        <div className="flex flex-col items-center justify-center w-full min-h-screen">
            <div className="flex flex-col items-center justify-center p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4">
                <input 
                    type="text" 
                    placeholder="Enter class name" 
                    value={className} 
                    onChange={(e) => setClassName(e.target.value)} 
                    className="p-2 border rounded w-full text-slate-900"
                />
                <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
                
                <button
                    onClick={uploadFile}
                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                    Upload
                </button>
                {message && <p className="text-center text-gray-700">{message}</p>}
            </div>
        </div>
    );
};  
export default page

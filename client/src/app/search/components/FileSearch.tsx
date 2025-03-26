"use client";

import React, { useEffect, useState } from 'react';
import './FileSearch.css';

interface File {
  className: string;
  id: number;
  uploaded_by: string;
  file_url: string;
  fileName: String;

}

const FileSearch: React.FC = () => {
  
  const [fileList, setFileList] = useState<File[] | null>(null);
  const [text, setText] = useState<string>('');
  

  const getFiles = async function (className : string|null, token:string) {
    if (!className) return;
    console.log(className)
    const res = await fetch("/api/search", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      credentials: "include",
      body: JSON.stringify({className:className, token:token}),
    })

    const data = await res.json();
    console.log(data)
    console.log(data.message)
    data.success && setFileList(data.message)
  }

  useEffect(() => {
    const queryParams = new URLSearchParams(window.location.search);
    const query = queryParams.get("q");
    console.log(query); // "Math 224"

    const token = document.cookie
        .split("; ")
        .find(row => row.startsWith("access_token="))?.split("=")[1];
    console.log(token)
    if (!token) {
       console.log("No token found");
       return;
  }
    getFiles(query,token);   
    
  },[])

  return (
    <div className='bg-gray-900 min-h-screen'>
      <div className="title">
        <h1>File Finder</h1>
      </div>
      <div className="input__wrapper text-slate-900">
        <input
          type="text"
          placeholder="Search File"
          value={text}
          onChange={(e) => {
            setText(e.target.value);

            if (!e.target.value) {
              setFileList(fileList);
            }
          }}
        />
        <button onClick={() => getFiles(text)}>
          Search
        </button>
      </div>

      <div className="body">
        {fileList?.length === 0 && (
          <div className="notFound">No File Found</div>
        )}

        {fileList?.length > 0 && fileList?.map((file, index) => {
          return (
            <div className="body__item" key={index}>
              <h3>Name: {file.fileName}</h3>
              <p>Type: pdf</p>
                <p className="">className : {file.className}</p>
                <p className="">Uploaded by : {file.uploaded_by}</p>
                <a href={file.file_url} download={file.file_url} target="_blank" className="download-link text-blue-500">View</a>

            </div>
            
          );
        })}
      </div>
    </div>
  );
};

export default FileSearch;
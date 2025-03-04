"use client";

import React, { useState } from 'react';
import './FileSearch.css';

interface File {
  name: string;
  type: string;
  url: string;
}

const FileSearch: React.FC = () => {
  const files: File[] = [
    {
      name: "project_proposal.pdf",
      type: "PDF",
      url: "/files/project_proposal.pdf"
    },
    {
      name: "financial_report.xlsx",
      type: "Excel",
      url: "/files/financial_report.xlsx"
    },
    {
      name: "team_photo.jpg",
      type: "JPEG",
      url: "/files/team_photo.jpg"
    },
    {
      name: "user_manual.docx",
      type: "DOCX",
      url: "/files/user_manual.docx"
    },
    {
      name: "presentation.pptx",
      type: "PPTX",
      url: "/files/presentation.pptx"
    }
  ];
  
  const [fileList, setFileList] = useState<File[]>(files);
  const [text, setText] = useState<string>('');

  const handleOnClick = () => {
    if (text.trim()) {
      const findFiles = files.filter((file) => 
        file.name.toLowerCase().includes(text.toLowerCase())
      );
      
      setFileList(findFiles);
    }
  };

  return (
    <div className='bg-gray-900 min-h-screen'>
      <div className="title">
        <h1>User Find</h1>
      </div>
      <div className="input__wrapper">
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
        <button disabled={!text.trim()} onClick={handleOnClick}>
          Search
        </button>
      </div>

      <div className="body">
        {fileList.length === 0 && (
          <div className="notFound">No User Found</div>
        )}

        {fileList.length > 0 && fileList.map((file, index) => {
          return (
            <div className="body__item" key={index}>
              <h3>Name: {file.name}</h3>
              <p>Type: {file.type}</p>
              <a 
                  href={file.url} 
                  download={file.name} 
                  className="download-link text-blue-500"
                >
                  Download
                </a>
            </div>
            
          );
        })}
      </div>
    </div>
  );
};

export default FileSearch;
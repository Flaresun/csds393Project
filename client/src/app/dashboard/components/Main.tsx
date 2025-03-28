"use client";
import React, { useState } from 'react';
import { X, Eye, Download, FileText, FileImage, FileAudio, File } from 'lucide-react';

// Define TypeScript interfaces
interface Classes {
  icon: string;
  name: string;
  role: string;
  color: string;
}

interface FileFolder {
  icon: string;
  name: string;
  files: number;
}

interface FileItem {
  icon: string;
  name: string;
  type: string;
  size: string;
  url: string;
}

const FileViewModal: React.FC<{ 
  file: FileItem | null, 
  onClose: () => void 
}> = ({ file, onClose }) => {
  if (!file) return null;

  const handleDownload = () => {
    fetch(file.url)
      .then(response => response.blob())
      .then(blob => {
        const link = document.createElement('a');
        const url = window.URL.createObjectURL(blob);
        
        link.href = url;
        link.download = `${file.name}.${file.type.split(' ')[0].toLowerCase()}`;
        
        document.body.appendChild(link);
        link.click();
      })
      .catch(error => {
        console.error('Download failed:', error);
        alert('Download failed. Please try again.');
      });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div className="bg-slate-800 rounded-lg p-6 w-96 relative">
        <button 
          onClick={onClose} 
          className="absolute top-4 right-4 text-gray-300 hover:text-white"
        >
          ✕
        </button>
        
        <div className="flex flex-col items-center">
          <div className="text-6xl mb-4">{file.icon}</div>
          <h2 className="text-xl font-semibold text-gray-200">{file.name}</h2>
          <p className="text-gray-400">{file.type}</p>
          <p className="text-gray-400 mt-2">{file.size}</p>
        </div>

        <div className="mt-6 flex justify-center space-x-4">
          <button 
            className="bg-blue-600 text-white px-4 py-2 rounded"
            onClick={() => window.open(file.url, '_blank')}
          >
            Preview
          </button>
          <button 
            className="bg-green-600 text-white px-4 py-2 rounded"
            onClick= {handleDownload}
          >
            Download
          </button>
        </div>
      </div>
    </div>
  );
};

const Main: React.FC = () => {
  // State for categories
  const [classes] = useState<Classes[]>([
    { icon: "➕", name: "Math 224: Differential Equations", role: "Student", color: "#4B2C83" },
    { icon: "📱", name: "CSDS 393: Software Engineering", role: "Student", color: "#6A3D9B" },
    { icon: "🧲", name: "PHYS 221: Modern Physics", role: "Student", color: "#9B59B6" },
    { icon: "🔢", name: "CSDS 343: Theoretical Computer Science", role: "Student", color: "#B285D5" },
  ]);

  // State for file folders
  const [folders] = useState<FileFolder[]>([
    { icon: "📊", name: "Work", files: 820 },
    { icon: "👤", name: "Personal", files: 115 },
    { icon: "🎓", name: "School", files: 65 },
    { icon: "📦", name: "Archive", files: 21 },
  ]);

  // State for recent files
  const [recentFiles] = useState<FileItem[]>([
    { icon: "📷", name: "IMG_100000", type: "PNG file", size: "5 MB", url:"https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/1966.png" },
    { icon: "📄", name: "SRS Document", type: "PDF file", size: "1.3 MB", url:"" },
    { icon: "🔊", name: "Lecture 2", type: "MP3 file", size: "21 MB", url:"" },
    { icon: "📄", name: "Design Document", type: "DOCx file", size: "1.2 MB", url:"" },
  ]);

<<<<<<< HEAD
  const [selectedFile, setSelectedFile] = useState<FileItem | null>(null);
=======

  
>>>>>>> 9cb608f211d2321407332d137a8c2ab8b510e212

  return (
    <div className="flex bg-slate-900">


      {/* Main content */}
      <div className="flex-1 p-6 overflow-y-auto">

        {/* Categories */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-300">My Classes</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {classes.map((category, index) => (
              <button
                key={index}
                className="p-4 rounded-lg text-white"
                style={{ backgroundColor: category.color }}
              >
                <div className="text-2xl mb-2">{category.icon}</div>
                <p className="font-semibold">{category.name}</p>
                <p className="text-sm opacity-80 mt-2">{category.role}</p>
              </button>
            ))}
            <div className="p-4 bg-slate-700 flex-col rounded-lg shadow-sm flex items-center justify-center">
              <div className="text-2xl text-blue-500">+</div>
              
            </div>
          </div>
        </div>

        {/* Folders section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-300">My Folders</h2>
          <div className="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {folders.map((folder, index) => (
              <button key={index} className="p-4 bg-slate-700 rounded-lg shadow-sm">
                <div className="text-2xl mb-2">{folder.icon}</div>
                <div className="font-semibold text-white">{folder.name}</div>
                <div className="text-sm text-gray-300">{folder.files} files</div>
              </button>
            ))}
            <button className="p-4 bg-gray-700 rounded-lg shadow-sm flex items-center justify-center">
              <span className="text-2xl text-blue-500">+</span>
            </button>
          </div>
        </div>

        {/* Recent files */}
        <div>
          <h2 className="text-xl font-semibold mb-4 text-gray-300">Recent files</h2>
          <div className="space-y-2">
            {recentFiles.map((file, index) => (
              <div 
              key={index} 
              className="bg-gray-500 p-4 rounded-lg shadow-sm flex items-center cursor-pointer hover:bg-gray-600 transition"
              onClick={() => setSelectedFile(file)}
              >
                <div className="w-10 h-10 flex items-center justify-center rounded-lg mr-4" style={{ backgroundColor: index === 0 ? '#7377F8' : index === 1 ? '#E75D8D' : index === 2 ? '#4D7CFE' : '#3DBBB3' }}>
                  <span className="text-white">{file.icon}</span>
                </div>
                <div className="flex-grow">
                  <div className="font-medium text-gray-300">{file.name}</div>
                  <div className="text-sm text-gray-300">{file.type}</div>
                </div>
                <div className="text-gray-500 mr-4">{file.size}</div>
                <div className="text-blue-500 mr-4">🔗</div>
                <div className="text-gray-400">⋯</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    
    {/* File View Modal */}
    {selectedFile && (
        <FileViewModal 
          file={selectedFile} 
          onClose={() => setSelectedFile(null)} 
        />
      )}
      
    </div>
  );
};

export default Main;

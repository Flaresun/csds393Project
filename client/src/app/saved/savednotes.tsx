"use client";
import React, { useState } from 'react';

const SavedNotes: React.FC = () => {

    interface FileItem {
        icon: string;
        name: string;
        type: string;
        size: string;
    }

    // State for recent files
    const [recentFiles] = useState<FileItem[]>([
        { icon: "📷", name: "IMG_100000", type: "PNG file", size: "5 MB" },
        { icon: "📄", name: "SRS Document", type: "PDF file", size: "1.3 MB" },
        { icon: "🔊", name: "Lecture 2", type: "MP3 file", size: "21 MB" },
        { icon: "📄", name: "Design Document", type: "DOCx file", size: "1.2 MB" },
    ]);


    return (
        <div className="flex bg-slate-900 min-h-screen">
            <div className="flex-1 p-6 overflow-y-auto">
                <div>
                    <h2 className="text-xl font-semibold mb-4 text-gray-300">Saved files</h2>
                    <div className="space-y-2">
                        {recentFiles.map((file, index) => (
                        <div key={index} className="bg-gray-500 p-4 rounded-lg shadow-sm flex items-center">
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
        </div>
    );
    
};

export default SavedNotes;

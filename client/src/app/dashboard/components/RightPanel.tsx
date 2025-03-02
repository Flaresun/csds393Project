import React, { useState } from 'react';

interface SharedFolder {
    name: string;
    users: number;
    color: string;
  }

const RightPanel: React.FC = () => {

    const [sharedFolders] = useState<SharedFolder[]>([
        { name: "Unit 1", users: 2, color: "#D1EAE9" },
        { name: "Unit 2", users: 1, color: "#E6E6FA" },
        { name: "Unit 3", users: 2, color: "#FADBD8" },
      ]);
    
    // Storage info
    const storageUsed = 0;
    const storageTotal = 100;
    const storagePercent = 100;

    return (
      <div className="flex flex-col bg-slate-900">
        {/* Right sidebar */}
        <div className="w-64 p-6 bg-white border-l border-gray-200">
        {/* Add new files button */}
        <div className="mb-10">
            <button className="w-full bg-white border border-gray-300 rounded-lg py-4 px-6 flex flex-col items-center justify-center text-blue-500 hover:bg-gray-50">
            <span className="text-2xl mb-2">📤</span>
            <span>Add new files</span>
            </button>
        </div>
        
        {/* Storage info */}
        <div className="mb-10">
            <div className="flex justify-between items-center mb-2">
            <h3 className="font-semibold text-gray-700">Your storage</h3>
            <span className="text-green-500">{storagePercent}% left</span>
            </div>
            <div className="text-sm text-gray-500 mb-2">
            {storageUsed} GB of {storageTotal} GB are used
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${100 - storagePercent}%` }}></div>
            </div>
        </div>
        
        {/* Shared folders */}
        <div>
            <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold text-gray-700">Recent folders</h3>
            </div>
            <div className="space-y-3">
            {sharedFolders.map((folder, index) => (
                <div 
                key={index} 
                className="p-3 rounded-lg flex justify-between items-center"
                style={{ backgroundColor: folder.color }}
                >
                <span>{folder.name}</span>
                <div className="flex -space-x-2">
                    {[...Array(folder.users)].map((_, i) => (
                    <div key={i} className="w-6 h-6 rounded-full border-2 border-white bg-gray-300 flex items-center justify-center text-xs">
                        👤
                    </div>
                    ))}
                </div>
                </div>
            ))}
            <button className="w-full py-2 text-center border border-gray-300 rounded-lg text-gray-500 hover:bg-gray-50">
                + Add more
            </button>
            </div>
        </div>

        </div>
      </div>
    );
};

export default RightPanel;
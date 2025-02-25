"use client";

import React, { useState } from 'react';
import Navbar from './Navbar';
import { FiHome, FiUpload, FiSearch, FiBookmark, FiSettings, FiMail, FiFileText, FiStar } from 'react-icons/fi';

// Type definitions
interface PDF {
  id: string;
  title: string;
  thumbnail: string;
  lastViewed: Date;
  viewCount: number;
}

interface Flashcard {
  id: string;
  title: string;
  subject: string;
  cardCount: number;
  usageCount: number;
}

const Dashboard2: React.FC = () => {
  // Sample data
  const [recentPDFs, setRecentPDFs] = useState<PDF[]>([
    { id: '1', title: 'CSDS 393: Software Engineering', thumbnail: '/api/placeholder/80/100', lastViewed: new Date('2025-02-24'), viewCount: 42 },
    { id: '2', title: 'CSDS 344: Computer Security', thumbnail: '/api/placeholder/80/100', lastViewed: new Date('2025-02-23'), viewCount: 28 },
    { id: '3', title: 'MATH 224: Elementary Differential Equations', thumbnail: '/api/placeholder/80/100', lastViewed: new Date('2025-02-22'), viewCount: 17 },
    { id: '4', title: 'ENGR 399: Impact of Engineering on Society', thumbnail: '/api/placeholder/80/100', lastViewed: new Date('2025-02-21'), viewCount: 36 },
  ]);

  return (
    <div className="flex flex-col h-screen bg-slate-900">
      {/* Navbar at top */}
      <Navbar />

      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <div className="w-64 bg-gray-800 shadow-md p-4 hidden md:block">
          <nav>
            <ul className="space-y-2 font-bold">
              <li>
                <a href="#" className="flex items-center p-2 text-slate-100 rounded hover:bg-blue-50 hover:text-blue-600">
                  <FiHome className="mr-3" />
                  <span>Home</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center p-2 text-slate-100 rounded hover:bg-blue-50 hover:text-blue-600">
                  <FiUpload className="mr-3" />
                  <span>Upload Notes</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center p-2 text-slate-100 rounded hover:bg-blue-50 hover:text-blue-600">
                  <FiSearch className="mr-3" />
                  <span>Browse Files</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center p-2 text-slate-100 rounded hover:bg-blue-50 hover:text-blue-600">
                  <FiBookmark className="mr-3" />
                  <span>Saved Notes</span>
                </a>
              </li>
              <li className="pt-4 border-t border-gray-200 mt-4">
                <a href="#" className="flex items-center p-2 text-slate-100 rounded hover:bg-blue-50 hover:text-blue-600">
                  <FiSettings className="mr-3" />
                  <span>Settings</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center p-2 text-slate-100 rounded hover:bg-blue-50 hover:text-blue-600">
                  <FiMail className="mr-3" />
                  <span>Contact Support</span>
                </a>
              </li>
            </ul>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-y-auto p-6">
          <h1 className="text-2xl font-bold text-slate-100 mb-6">Dashboard</h1>

          {/* Recently Viewed PDFs */}
          <section className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-slate-100">Recently Viewed Notes</h2>
              <a href="#" className="text-sm text-blue-600 hover:text-blue-800">View All</a>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {recentPDFs.map(pdf => (
                <div key={pdf.id} className="bg-white rounded-lg shadow overflow-hidden hover:shadow-md transition-shadow">
                  <div className="p-4 flex items-start">
                    <div className="flex-shrink-0 bg-gray-200 rounded">
                      {/* <img src={pdf.thumbnail} alt={pdf.title} className="h-20 w-16 object-cover" /> */}
                    </div>
                    <div className="ml-4">
                      <h3 className="text-sm font-medium text-gray-900 line-clamp-2">{pdf.title}</h3>
                      <p className="mt-1 text-xs text-gray-500">
                        Last viewed: {pdf.lastViewed.toLocaleDateString()}
                      </p>
                      <div className="mt-2 flex items-center text-xs text-gray-500">
                        <FiFileText className="mr-1" />
                        <span>{pdf.viewCount} views</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>

        </div>
      </div>
    </div>
  );
};

export default Dashboard2;
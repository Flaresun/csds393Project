"use client";
import React from 'react'
import Navbar from './Navbar'
import { AppContent } from '@/context/AppContext';
import { useContext } from 'react'
import LeftPanel from './LeftPanel';
import Main from './Main';
import RightPanel from './RightPanel';

const Dashboard = () => {
      const {panel, setPanel} = useContext<any>(AppContent);
  
  return (
    <div>
        {/**Split 3 way. Navbar on top with search, notifications, profile, extras */}
        <Navbar />

        <div className="flex justify-start gap-x-20">
          <div className="mt-10 w-64">
            <LeftPanel panel={panel}/>
          </div>
          <Main />
          <div className="mt-10 w-64">
            <RightPanel />
          </div>
        </div>
        

        {/**Split 3 way. Main dashboard page. Top k recently viewed pdfs. Popular flashcards being reviewed. */}

        

    </div>
  )
}

export default Dashboard
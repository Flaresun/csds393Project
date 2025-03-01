"use client";
import React from 'react'
import Navbar from './Navbar'
import { AppContent } from '@/context/AppContext';
import { useContext } from 'react'
import LeftPanel from './LeftPanel';
import Main from './Main';

const Dashboard = () => {
      const {panel, setPanel} = useContext<any>(AppContent);
  
  return (
    <div>
        {/**Split 3 way. Navbar on top with search, notifications, profile, extras */}
        <Navbar />

        {/**Split 3 way. Leftbar with navigation tools. Like go upload a file, Go browse files. Saved files, home, settings, contact */}
        <div className="flex">
          <LeftPanel panel={panel}/>
          <Main />
        </div>
        

        {/**Split 3 way. Main dashboard page. Top k recently viewed pdfs. Popular flashcards being reviewed. */}

        

    </div>
  )
}

export default Dashboard
"use client";
import Options from './options';
import LeftPanel from '../dashboard/components/LeftPanel';
import { AppContent } from '@/context/AppContext';
import { useContext } from 'react'
import Navbar from '../dashboard/components/Navbar';
import Main from '../dashboard/components/Main';

const Page = () => {
    const {panel, setPanel} = useContext<any>(AppContent);

    return (
    <div className="bg-slate-900">
        {/**Split 3 way. Navbar on top with search, notifications, profile, extras */}
        <Navbar />

        <div className="flex overflow-y-auto">
            <LeftPanel panel={panel}/>
            <Options />
        </div>
        

        {/**Split 3 way. Main dashboard page. Top k recently viewed pdfs. Popular flashcards being reviewed. */}

        

    </div>
    );
};

export default Page
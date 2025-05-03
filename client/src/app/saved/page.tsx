"use client";
import SavedNotes from './savednotes';
import LeftPanel from '../dashboard/components/LeftPanel';
import { AppContent } from '@/context/AppContext';
import { useContext } from 'react'
import Navbar from '../dashboard/components/Navbar';

const Page = () => {
    const {panel, setPanel} = useContext<any>(AppContent);

    return (
    <div className="bg-slate-900">
        {/**Split 3 way. Navbar on top with search, notifications, profile, extras */}
        <Navbar />

        <div className="flex overflow-y-auto">
            <LeftPanel panel={panel}/>
            <SavedNotes />
        </div>
        

        {/**Split 3 way. Main dashboard page. Top k recently viewed pdfs. Popular flashcards being reviewed. */}

        

    </div>
    );
};

export default Page
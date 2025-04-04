"use client";
import Dashboard from './components/Dashboard';
import { AppContent } from '@/context/AppContext';
import React, { useContext, useEffect} from 'react'

const page = () => {
<<<<<<< HEAD

=======
  const {isValidSession} = useContext<any>(AppContent);
  useEffect(() => {
    isValidSession()
  })
>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8
  
  return (
    <div className='p-[2rem] bg-slate-900 min-h-screen'>
      <Dashboard/>
    </div>
  )
}

export default page;
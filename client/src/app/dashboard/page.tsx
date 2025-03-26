"use client";
import Dashboard from './components/Dashboard';
import { AppContent } from '@/context/AppContext';
import React, { useContext, useEffect} from 'react'

const page = () => {
  const {isValidSession} = useContext<any>(AppContent);
  useEffect(() => {
    isValidSession()
  })
  
  return (
    <div className='p-[2rem] bg-slate-900 min-h-screen'>
      <Dashboard/>
    </div>
  )
}

export default page;
"use client";
import UserFind from './components/FileSearch';
import { AppContent } from '@/context/AppContext';
import React, { useContext, useEffect} from 'react'
const page = () => {
  const {isValidSession} = useContext<any>(AppContent);

  useEffect(() => {
    isValidSession()
  })
  return (
    <div>
      <UserFind />
    </div>
  )
}

export default page

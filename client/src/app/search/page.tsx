"use client";
import UserFind from './components/FileSearch';
import { AppContent } from '@/context/AppContext';
import React, { useContext, useEffect} from 'react'
const page = () => {

  return (
    <div>
      <UserFind />
    </div>
  )
}

export default page
"use client";
import UserFind from './components/FileSearch';
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
    <div>
      <UserFind />
    </div>
  )
}

<<<<<<< HEAD
export default page
=======
export default page
>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8

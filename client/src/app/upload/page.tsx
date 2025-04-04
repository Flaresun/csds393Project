"use client";
<<<<<<< HEAD
import Uploader from "./components/uploader"
import { AppContent } from '@/context/AppContext';
import React, { useContext, useEffect} from 'react'
function UploadPage() {

=======
import Uploader from "./components/uploader";
import { AppContent } from '@/context/AppContext';
import React, { useContext, useEffect} from 'react'
function UploadPage() {
    const {isValidSession} = useContext<any>(AppContent);
    useEffect(() => {
        isValidSession()
      })
>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8
    
    return (
        <Uploader />
    )
}

export default UploadPage;
<<<<<<< HEAD
=======

>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8

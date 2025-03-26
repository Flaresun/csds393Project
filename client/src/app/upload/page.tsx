"use client";
import Uploader from "./components/uploader";
import { AppContent } from '@/context/AppContext';
import React, { useContext, useEffect} from 'react'
function UploadPage() {
    const {isValidSession} = useContext<any>(AppContent);
    useEffect(() => {
        isValidSession()
      })
    
    return (
        <Uploader />
    )
}

export default UploadPage;


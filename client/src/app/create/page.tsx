"use client";
import React from 'react';
import CreateNotes from './components/CreateNotes';
import { useContext, useEffect } from "react";
import { useRouter } from 'next/navigation'
import { AppContent } from "@/context/AppContext";

const page = () => {
  const {userRole} = useContext<any>(AppContent);
  const router = useRouter();
  
  useEffect(() => {
    if (userRole != "faculty") {
      router.push("/dashboard");
    }
  },[userRole])

  return (
    <div>
        <CreateNotes />
    </div>
  )
}

export default page
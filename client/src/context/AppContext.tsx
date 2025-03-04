"use client";
import { createContext, useEffect, useState } from "react";
import React from 'react';
 

export const AppContent = createContext<any>(null);

export const AppContextProvider = (props:any) => {
    {/**Need a LeftPanel Context */}
    const [panel, setPanel] = useState<boolean>(true);
    {/**Need a Theme Context */}
    {/**Need a Auth Context */}
    const [userEmail, setUserEmail] = useState<string|null>(null);
    const value : any = { 
        panel, setPanel,
        userEmail, setUserEmail
    }
    return (
        <AppContent.Provider value={value}>
            {props.children}
        </AppContent.Provider>
    )
}
"use client";
import { createContext, useEffect, useState } from "react";
import React from 'react';
import { useRouter } from 'next/navigation'


export const AppContent = createContext<any>(null);

export const AppContextProvider = (props:any) => {
    {/**Need a LeftPanel Context */}
    const [panel, setPanel] = useState<boolean>(true);
    const [userEmail, setUserEmail] = useState<string|null>(null);
    const [isAuth, setIsAuth] = useState<boolean>(false)
    const router = useRouter();

    {/**Need a Theme Context */}

    const isValidSession = () => {
        if (!isAuth) {
            router.push("/"); 
        }
    }

    const validateUser = async (token : string|undefined) : Promise<any> => {
        if (!token) {
            console.log("No token");
            return;
        };
        try {
            const res = await fetch("/api/verifyUser", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ token:token}),
                credentials: 'include',
                })
        
                const data = await res.json();
                console.log(data)
                setIsAuth(data.success)
                return data.success 
        } catch {

        }
    }
    
    useEffect(() => {   
        const token : string|undefined = document.cookie
            .split("; ")
            .find(row => row.startsWith("access_token="))?.split("=")[1];
        validateUser(token)

      })

    
    const value : any = { 
        panel, setPanel,
        userEmail, setUserEmail,
        isAuth,setIsAuth,
        isValidSession
    }
    return (
        <AppContent.Provider value={value}>
            {props.children}
        </AppContent.Provider>
    )
}
"use client";
import { createContext, useEffect, useState } from "react";
import React from 'react';
import { useRouter } from 'next/navigation'


export const AppContent = createContext<any>(null);

export const AppContextProvider = (props:any) => {
    {/**Need a LeftPanel Context */}
    const [panel, setPanel] = useState<boolean>(true);
<<<<<<< HEAD
    const [userEmail, setUserEmail] = useState<string | null>(null);
    const [isAuth, setIsAuth] = useState<boolean>(false);
    const router = useRouter();
  
    const validateUser = async (token: string | undefined): Promise<boolean> => {
      if (!token) {
        console.log("No token");
        return false;
      }
      try {
        const res = await fetch("/api/verifyUser", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ token: token }),
          credentials: 'include',
        });
  
        const data = await res.json();
        console.log(data);
        console.log(data.success);
        setIsAuth(data.success);
        return data.success;
      } catch (error) {
        console.error("Error during validation", error);
        return false;
      }
    };
  
    useEffect(() => {
      const token: string | undefined = document.cookie
        .split("; ")
        .find((row) => row.startsWith("token="))?.split("=")[1];
  
      const checkAuth = async () => {
        const isValid = await validateUser(token);
        if (!isValid) {
          router.push("/");
        }
      };
  
      checkAuth();
    }, [isAuth, router]);

=======
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

>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8
    
    const value : any = { 
        panel, setPanel,
        userEmail, setUserEmail,
        isAuth,setIsAuth,
<<<<<<< HEAD
=======
        isValidSession
>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8
    }
    return (
        <AppContent.Provider value={value}>
            {props.children}
        </AppContent.Provider>
    )
}
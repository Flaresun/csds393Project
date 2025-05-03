"use client";
import { createContext, useEffect, useState } from "react";
import React from 'react';
import { useRouter } from 'next/navigation'

// Context to manage application-wide state
export const AppContent = createContext<any>(null);

/**
 * AppContextProvider component manages the state and logic for the entire app.
 * It includes authentication, user roles, and a panel state.
 * 
 * @param props - Children components that will consume this context.
 */
export const AppContextProvider = (props: any) => {
    // State for managing the left panel visibility
    const [panel, setPanel] = useState<boolean>(true);

    // State for managing the user's email
    const [userEmail, setUserEmail] = useState<string | null>(null);

    // State for checking if the user is authenticated
    const [isAuth, setIsAuth] = useState<boolean>(false);

    // State for managing the user's role (student or faculty)
    const [userRole, setUserRole] = useState<"student" | "faculty">("student");

    // Router instance for navigation
    const router = useRouter();

    /**
     * Fetches the role of the user based on their email.
     * It is called when the user email is updated.
     */
    const getRole = async () => {
        if (!userEmail) return;

        const res = await fetch("/api/getRole", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: userEmail }),
        });

        const data = await res.json();
        console.log(data);
        setUserRole(data.role);
    }

    /**
     * Validates the user's token and sets the authentication state.
     * 
     * @param token - The JWT token used to verify the user.
     * @returns Promise<boolean> - Resolves to true if valid, false otherwise.
     */
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
            setUserEmail(data.user);
            return data.success;
        } catch (error) {
            console.error("Error during validation", error);
            return false;
        }
    };

    useEffect(() => {
        /**
         * Checks the user's authentication status based on the token.
         * Redirects to the login page if the user is not authenticated.
         */
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

    useEffect(() => {
        /**
         * Calls `getRole` whenever the user's email changes.
         */
        console.log(userEmail);
        getRole();
    }, [userEmail]);

    const value: any = {
        panel, setPanel,
        userEmail, setUserEmail,
        isAuth, setIsAuth,
        userRole, setUserRole
    }

    return (
        <AppContent.Provider value={value}>
            {props.children}
        </AppContent.Provider>
    )
}

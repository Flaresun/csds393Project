"use client";
import { useRouter } from 'next/navigation'
import React, { useState } from 'react'
import { FiHome, FiUpload, FiSearch, FiBookmark, FiSettings, FiMail, FiFileText, FiStar } from 'react-icons/fi';


const LeftPanel = (props : any) => {

    interface activeTypes {
        type : "Home" | "Upload" | "Browse" | "Saved" | "Settings" | "Support"
    }

    const itemSize :number = 30;
    const [active, setActive] = useState<string>("Home");
    const router = useRouter();

    const handleActive = (e : any) => {
        const word : string = e.target.innerText
        console.log(e)
        setActive(word)
        // Navigate to page based off innerText
        router.push(word.split(" ")[0].toLowerCase())
    }

    return (
        
        <div className={`z-10 text-nowrap`} >
            {props.panel && (

            
            <div className="flex flex-col items-start justify-center text-center text-slate-500 text-xl w-full ">
                <div onClick={(e)=> handleActive(e)} className={`flex flex-row items-start justify-start text-center p-2 ${active==="Home" && "bg-slate-200 rounded-md w-full " } mb-5 cursor-pointer`}> 
                    <FiHome size={itemSize}/>
                    <p className="ml-4">Home</p>
                </div>
                <div onClick={(e)=> handleActive(e)} className={`flex flex-row items-start justify-start text-center p-2 ${active==="Upload Notes" && "bg-slate-200 rounded-md w-full" } mb-5 cursor-pointer`}> 
                    <FiUpload size={itemSize}/>
                    <p className="ml-4">Upload Notes</p>
                </div>
                <div onClick={(e)=> handleActive(e)} className={`flex flex-row items-start justify-start text-center p-2 ${active==="Browse Files" && "bg-slate-200 rounded-md w-full" } mb-5 cursor-pointer`}> 
                    <FiSearch  size={itemSize}/>
                    <p className="ml-4">Browse Files</p>
                </div>
                <div onClick={(e)=> handleActive(e)} className={`flex flex-row items-start justify-start text-center p-2 ${active==="Saved Notes" && "bg-slate-200 rounded-md w-full" } mb-5 cursor-pointer`}> 
                    <FiBookmark  size={itemSize}/>
                    <p className="ml-4">Saved Notes</p>
                </div>
                <div onClick={(e)=> handleActive(e)} className={`flex flex-row items-start justify-start text-center p-2 ${active==="Settings" && "bg-slate-200 rounded-md w-full" } mb-5 cursor-pointer`}> 
                    <FiSettings  size={itemSize}/>
                    <p className="ml-4">Settings</p>
                </div>
                <div onClick={(e)=> handleActive(e)} className={`flex flex-row items-start justify-start text-center p-2 ${active==="Support" && "bg-slate-200 rounded-md w-full" } mb-5 cursor-pointer`}> 
                    <FiMail   size={itemSize}/>
                    <p className="ml-4">Support</p>
                </div>
            </div>
            )}
        </div>
    )
}

export default LeftPanel
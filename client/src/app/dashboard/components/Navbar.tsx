"use client";
import React from 'react'
import { RxHamburgerMenu } from "react-icons/rx";
import { assets } from '@/assets/asset';
import { CiSearch } from "react-icons/ci";
import Image from 'next/image';
import { useState } from 'react';
import { CiUser } from "react-icons/ci";
import { MdOutlineLightMode } from "react-icons/md";
import { MdOutlineDarkMode } from "react-icons/md";
import { IoIosNotificationsOutline } from "react-icons/io";
import { MdOutlinePrivacyTip } from "react-icons/md";
import { IoIosLogOut } from "react-icons/io";

const Navbar = () => {
    const logoWidth : number = 100;
    const [profileModule, setProfileModule] = useState<boolean>(false);
  return (
    <div className="flex flex-col">        

        <div className='flex flex-row items-center justify-between text-xl'>
            <div className="flex flex-row items-center justify-between">
                <button className=""><RxHamburgerMenu className="text-slate-500" size={50}/></button>
                <Image src={assets.logo} alt="Logo" width={logoWidth}/>
            </div>

            <div className="hidden sm:flex border items-start justify-start text-center bg-gray-400 text-slate-900 rounded-md p-2">
                <CiSearch size={30} className='cursor-pointer'/>
                <input type="text" className="pl-2 bg-transparent border-none focus:outline-none placeholder-slate-900 sm:w-full lg:w-[40rem]" placeholder='Search for files' />
            </div>
            
            

            <div className="flex">
                <div onClick={() => setProfileModule((prev) => !prev)}className="flex border rounded-full px-4 py-2 bg-gray-400 text-slate-900 cursor-pointer">
                    E
                    {profileModule && (
                    <div className="fixed top-20 right-8 px-5 bg-blue-500 text-2xl rounded-lg py-5">
                        <div className="flex items-center justify-center pb-5">
                            <p className="border rounded-full px-4 py-2 bg-gray-400 text-slate-900 cursor-pointer mr-5">E</p>
                            <div className="flex flex-col text-lg font-semibold">
                                <p className="">Name : John Doe</p>
                                <p className="text-sm">Email : email@gmail.com</p>
                            </div>
                        </div>
                        <div className="flex w-full bg-slate-900 h-[2px]"></div>
                        
                        <div className="flex flex-col items-start justify-start text-center font-medium">
                            <div className="flex items-center text-center justify-start transition-all ease-in-out hover:bg-gray-400 w-full rounded-md py-2">
                                <CiUser size={25}/>
                                <p className="ml-2">Profile</p>
                            </div>
                            <div className="flex items-center text-center justify-start transition-all ease-in-out hover:bg-gray-400 w-full rounded-md py-2">
                                <MdOutlineLightMode size={25}/>
                                <p className="ml-2">Light Mode</p>
                            </div>
                            <div className="flex items-center text-center justify-start hover:bg-gray-400 w-full rounded-md py-2">
                                <IoIosNotificationsOutline size={25}/>
                                <p className="ml-2">Notifications</p>
                            </div>
                            <div className="flex items-center text-center justify-start transition-all ease-in-out hover:bg-gray-400 w-full rounded-md py-2">
                                <MdOutlinePrivacyTip size={25}/>
                                <p className="ml-2">Privacy</p>
                            </div>
                            <div className="flex items-center text-center justify-start transition-all ease-in-out hover:bg-gray-400 w-full rounded-md py-2">
                                <IoIosLogOut size={25}/>
                                <p className="ml-2">Logout</p>
                            </div>
                        </div>
                        
                    </div>
                    )}
                    
                </div>
            </div>

            

        </div>
        {/**Search bar for small screens */}
        <div className="flex sm:hidden border items-center justify-start text-center bg-gray-400 text-slate-900 rounded-md mt-5 p-2">
                <CiSearch size={30} className='cursor-pointer'/>
                <input type="text" className="pl-2 bg-transparent border-none focus:outline-none placeholder-slate-900 w-full" placeholder='Search for files' />
        </div>
    </div>
  )
}

export default Navbar
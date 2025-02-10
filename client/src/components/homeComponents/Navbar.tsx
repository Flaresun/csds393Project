"use client";
import React, { useState } from 'react';
import {assets} from "../../assets/asset.js";
import Image from 'next/image';
import { RxHamburgerMenu } from "react-icons/rx";
import { IoClose } from "react-icons/io5";

const Navbar = () => {
  const itemSize : number = 40; 
  const [open, setOpen] = useState<boolean>(false);
  const handleClick = () : void => {
        setOpen((prev) => !prev)
  }
  return (
    <div className="flex sm:flex-row items-center justify-between ">
        <div className="flex">
            <Image
             src={assets.logo}
             alt="Logo"
             width={200}
             />
        </div>
        <div id="box-gradient" className="hidden lg:flex flex-row items-center justify-center border text-sm sm:text-xl rounded-3xl px-6 py-3">
            <p className="cursor-pointer mr-10">Home</p>
            <p className="cursor-pointer mr-10">Team</p>
            <p className="cursor-pointer mr-10">Product</p>
            <p className="cursor-pointer mr-10">Customers</p>
            <p className="cursor-pointer ">Pricing</p>

        </div>
        <div className="hidden lg:flex text-2xl">
            <button className="bg-slate-100 dark:text-slate-900 text-slate-100 rounded-full p-4 active:scale-95 transition-all">Get Started</button>
        </div>
        <div className="flex items-center justify-center text-center lg:hidden">

            {open ? (
            <>
            <IoClose size={itemSize} onClick={handleClick}/>
            <div className="fixed top-24 right-5 p-2 bg-slate-900">
                <p className="cursor-pointer mb-1 active:bg-slate-200 active:text-slate-900 px-2">Home</p>
                <p className="cursor-pointer mb-1 active:bg-slate-200 active:text-slate-900">Product</p>
                <p className="cursor-pointer mb-1 active:bg-slate-200 active:text-slate-900">Resources</p>
                <p className="cursor-pointer mb-1 active:bg-slate-200 active:text-slate-900">Customers</p>
                <p className="cursor-pointer active:bg-slate-200 active:text-slate-900">Pricing</p>
            </div>
            </>
            ) : (
                <RxHamburgerMenu size={itemSize} onClick={handleClick}/>

            )}

            
        </div>

    </div>
  )
}

export default Navbar;
"use client";
import React, { useEffect, useState } from 'react';
import {assets} from "../assets/asset.js";
import Image from 'next/image';
import { RxHamburgerMenu } from "react-icons/rx";
import { IoClose } from "react-icons/io5";
import { useRouter } from 'next/navigation'

const Navbar = () => {
  const itemSize : number = 40; 
  const [open, setOpen] = useState<boolean>(false);
  const handleClick = () : void => {
        setOpen((prev) => !prev)
  }
  const router = useRouter();
  useEffect(() => {
    window.addEventListener('scroll', (e) => {
        setOpen(false)
      })
  },[])
  
  return (
    <div className="flex sm:flex-row items-center justify-between ">
        <div className="flex">
            <Image
             src={assets.logo}
             alt="Logo"
             width={200}
             />
        </div>
        <div id="box-gradient" className="hidden lg:flex flex-row items-center justify-center border-4 border-violet-500 text-sm sm:text-xl rounded-3xl px-6 py-3">
            <a href="#hero" className="cursor-pointer mr-10">Home</a>
            <a href="#team" className="cursor-pointer mr-10">Team</a>
            <a href="#product" className="cursor-pointer mr-10">Product</a>
            <a href="#customers" className="cursor-pointer mr-10">Customers</a>
            <a href="#footer" className="cursor-pointer ">Footer</a>

        </div>
        <div className="hidden lg:flex text-2xl">
            <button onClick={()=> router.push("/login")} className="bg-slate-100 dark:text-slate-900 text-slate-100 rounded-full p-4 active:scale-95 transition-all">Get Started</button>
        </div>
        <div className="flex items-center justify-center text-center lg:hidden">

            {open ? (
            <>
            <IoClose size={itemSize} onClick={handleClick}/>
            <div className="fixed top-24 right-5 p-2 bg-slate-900 flex flex-col">
                <a href="#hero" className="cursor-pointer mb-1 active:bg-slate-200 active:text-slate-900 px-2">Home</a>
                <a href="#team" className="cursor-pointer mb-1 active:bg-slate-200 active:text-slate-900">Product</a>
                <a href="#product" className="cursor-pointer mb-1 active:bg-slate-200 active:text-slate-900">Resources</a>
                <a href="#customers" className="cursor-pointer mb-1 active:bg-slate-200 active:text-slate-900">Customers</a>
                <a href="#footer" className="cursor-pointer active:bg-slate-200 active:text-slate-900">Pricing</a>
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
"use client";
import React, { useEffect, useState } from 'react';
import { assets } from "../assets/asset.js";
import Image from 'next/image';
import { RxHamburgerMenu } from "react-icons/rx";
import { IoClose } from "react-icons/io5";
import { useRouter } from 'next/navigation';

// Navbar component to display the site's navigation bar with a responsive design
const Navbar = () => {
  // Set the size for the hamburger menu and close icons
  const itemSize: number = 40; 
  
  // State for tracking whether the mobile menu is open or closed
  const [open, setOpen] = useState<boolean>(false);

  // Handle toggle of mobile menu
  const handleClick = (): void => {
    setOpen((prev) => !prev);
  }

  // Router hook for navigation
  const router = useRouter();

  // Close the mobile menu when the user scrolls
  useEffect(() => {
    window.addEventListener('scroll', (e) => {
      setOpen(false);
    })
  }, []);
  
  return (
    <div className="flex sm:flex-row items-center justify-between ">
      
      {/* Logo section */}
      <div className="flex">
        <Image
          src={assets.logo}
          alt="Logo"
          width={200}
        />
      </div>
      
      {/* Desktop navigation links */}
      <div id="box-gradient" className="hidden text-slate-100 lg:flex flex-row items-center justify-center border text-sm sm:text-xl rounded-3xl px-6 py-3">
        <a href="#hero" className="cursor-pointer mr-10">Home</a>
        <a href="#team" className="cursor-pointer mr-10">Team</a>
        <a href="#product" className="cursor-pointer mr-10">Product</a>
        <a href="#customers" className="cursor-pointer mr-10">Customers</a>
        <a href="#footer" className="cursor-pointer ">Footer</a>
      </div>

      {/* Desktop Get Started button */}
      <div className="hidden lg:flex text-2xl">
        <button onClick={() => router.push("/login")} className="bg-slate-100 dark:text-slate-900 text-slate-900 rounded-full p-4 active:scale-95 transition-all">
          Get Started
        </button>
      </div>

      {/* Mobile menu toggle */}
      <div className="flex items-center justify-center text-center lg:hidden">
        
        {/* Display close button and menu links if open is true */}
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
          // Display hamburger menu if open is false
          <RxHamburgerMenu size={itemSize} onClick={handleClick}/>
        )}
      </div>
    </div>
  )
}

export default Navbar;

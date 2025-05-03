"use client";
import React from 'react'
import { assets } from "../assets/asset.js";
import Image, { StaticImageData } from 'next/image';
import "./Hero.css"
import { useRouter } from 'next/navigation';

// Hero component for the main section of the landing page
const Hero = () => {
  // Set the item size for logos
  const itemSize: number = 100;

  // Initialize the router for navigation
  const router = useRouter();

  // Array of logos to be used in the infinite slider
  const Logos: any = [
    <Image src={assets.cwru_logo} alt="CWRU Logo" width={itemSize} />,
    <Image src={assets.bgsu_logo} alt="BGSU Logo" width={itemSize} />,
    <Image src={assets.csu_logo} alt="CSU Logo" width={itemSize} />,
    <Image src={assets.dot_logo} alt="DOT Logo" width={itemSize} />,
    <Image src={assets.jcu_logo} alt="JCU Logo" width={itemSize} />,
    <Image src={assets.ksu_logo} alt="KSU Logo" width={itemSize} />,
    <Image src={assets.miami_logo} alt="Miami Logo" width={itemSize} />,
    <Image src={assets.osu_logo} alt="OSU Logo" width={itemSize} />,
    <Image src={assets.uoc_logo} alt="UOC Logo" width={itemSize} />,
    <Image src={assets.uot_logo} alt="UOT Logo" width={itemSize} />,
  ];

  return (
    <div id="hero" className='pt-20 px-[2rem] sm:px-[10rem]'>
      
      {/* Main heading and subheading */}
      <div className="flex flex-col items-center text-8xl text-slate-100 text-wrap">
        <div className="flex mt-5 items-center justify-center text-center">
          <p className="">Ace Your Studies with <span className="inline-block translate-y-4 whitespace-normal"><Image src={assets.logo} alt="Logo" width={270} /></span> </p>
        </div>
        
        <div className="flex text-xl sm:text-2xl mt-5 items-center justify-center text-center">
          <p className="">Our goal is to empower students worldwide with the help of advanced AI Features which will make studying much more efficient and beneficial for students hoping not only to ace their exams but also to understand their topics on a deeper level. </p>
        </div>

        {/* Buttons for navigation */}
        <div className="flex flex-col sm:flex-row text-2xl mt-5">
          <button onClick={() => router.push("/login")} className="bg-slate-100 text-slate-900 px-6 py-4 mr-5 rounded-md active:scale-95 transition-all mb-5 sm:mb-0">Get Started</button>
          <button onClick={() => router.push("/login")} className="hover:bg-slate-100 px-6 py-4 mr-5 hover:dark:text-slate-900 rounded-md active:scale-95 transition-all">Get in Touch</button>
        </div>

        {/* Subheading for working with college students */}
        <div className="flex flex-col text-3xl mt-20 mb-5">
          <p className="">Working with College Students all over Ohio</p>
        </div>

        {/* Infinite logo slider */}
        <div className="pb-20 relative m-auto w-full overflow-hidden bg-transparent before:absolute before:left-0 before:top-0 before:z-[2] before:h-full before:w-[100px] before:bg-[linear-gradient(to_right,black_0%,rgba(255,255,255,0)_100%)] before:content-[''] after:absolute after:right-0 after:top-0 after:z-[2] after:h-full after:w-[100px] after:-scale-x-100 after:bg-[linear-gradient(to_right,black_0%,rgba(255,255,255,0)_100%)] after:content-['']">
          <div className="animate-infinite-slider flex w-[calc(250px*10)]">
            {/* Display logos twice for the infinite scrolling effect */}
            {Logos.map((logo: any, index: number) => (
              <div className="slide flex w-[125px] items-center justify-center" key={index}>
                {logo}
              </div>
            ))}
            {Logos.map((logo: any, index: number) => (
              <div className="slide flex w-[125px] items-center justify-center" key={index}>
                {logo}
              </div>
            ))}
          </div>
        </div>
      </div>

    </div>
  )
}

export default Hero;

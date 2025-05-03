import Image from 'next/image'
import React from 'react'
import { assets } from "../assets/asset.js";

// Team component that displays team members with their names, roles, and pictures
const Team = () => {

  // Set the size of the profile pictures
  const itemSize: number = 200;

  return (
    <div id="team" className='px-[2rem] sm:px-[10rem] '>
        {/* Title of the section */}
        <p className="pt-10 flex items-center justify-center text-center text-5xl">Meet the Team</p>

        {/* Subtitle describing the team's experience */}
        <div className="pt-10 mb-10 flex items-center justify-center text-center ">
          <p className="text-2xl">With over 10+ years of combined experience in building, meet the team behind CNotes</p>
        </div>

        {/* Grid to display team members */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 ">
          {/* Team member card for Jason Lai */}
          <div className="flex flex-col items-center justify-center border rounded-md">
            <Image src={assets.jason_picture} alt="Jason Picture" width={itemSize/1.3}/>
            <div className="flex flex-col items-center justify-center text-center">
              <p className="text-2xl">Jason Lai</p>
              <p className="text-2xl text-sky-300">Frontend Team </p>
            </div>
          </div>

          {/* Team member card for Sean Brown */}
          <div className="flex flex-col items-center justify-center border rounded-md">
            <Image src={assets.sean_picture} alt="Sean Picture" width={itemSize}/>
            <div className="flex flex-col items-center justify-center text-center">
              <p className="text-2xl">Sean Brown</p>
              <p className="text-2xl text-green-300">Backend Team </p>
            </div>
          </div>

          {/* Team member card for Seth Omeike */}
          <div className="flex flex-col items-center justify-center border rounded-md">
            <Image src={assets.unknown_picture} alt="Seth Picture" width={itemSize}/>
            <div className="flex flex-col items-center justify-center text-center">
              <p className="text-2xl">Seth Omeike</p>
              <p className="text-2xl text-sky-300">Frontend Team </p>
            </div>
          </div>

          {/* Team member card for James Telzrow */}
          <div className="flex flex-col items-center justify-center border rounded-md">
            <Image src={assets.unknown_picture} alt="James Picture" width={itemSize}/>
            <div className="flex flex-col items-center justify-center text-center">
              <p className="text-2xl">James Telzrow</p>
              <p className="text-2xl text-green-300">Backend Team </p>
            </div>
          </div>
        </div>
    </div>
  )
}

export default Team;

import Image from 'next/image'
import React from 'react'
import {assets} from "../assets/asset.js";

const Team = () => {

  const itemSize : number = 200;


  return (
    <div id="team" className='px-[2rem] sm:px-[10rem] '>

        {/** Meet the Team is on the hero section and not here */}

        <div className="mb-10 flex items-center justify-center text-center ">
          <p className="text-2xl">With over 10+ years of combined experience in building, meet the team behind CNotes</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 ">
          <div className="flex flex-col  items-center justify-center border rounded-md">
            <Image src={assets.jason_picture} alt="Jason Picture" width={itemSize/1.3}/>
            <div className="flex flex-col items-center justify-center text-center">
              <p className="text-2xl">Jason Lai</p>
              <p className="text-2xl text-sky-300">Frontend Team </p>
            </div>
          </div>
          <div className="flex flex-col  items-center justify-center border rounded-md">
            <Image src={assets.sean_picture} alt="Sean Picture" width={itemSize}/>
            <div className="flex flex-col items-center justify-center text-center">
              <p className="text-2xl">Sean Brown</p>
              <p className="text-2xl text-green-300">Backend Team </p>
            </div>
          </div>
          <div className="flex flex-col  items-center justify-center border rounded-md">
            <Image src={assets.unknown_picture} alt="Jason Picture" width={itemSize}/>
            <div className="flex flex-col items-center justify-center text-center">
              <p className="text-2xl">Seth Omeike</p>
              <p className="text-2xl text-sky-300">Frontend Team </p>
            </div>
          </div>
          <div className="flex flex-col  items-center justify-center border rounded-md">
            <Image src={assets.unknown_picture} alt="Jason Picture" width={itemSize}/>
            <div className="flex flex-col items-center justify-center text-center">
              <p className="text-2xl">James Telzrow</p>
              <p className="text-2xl text-green-300">Backend Team </p>
            </div>
          </div>
        </div>
    </div>
  )
}

export default Team
import Image from 'next/image'
import React from 'react'
import {assets} from "../../assets/asset.js";

const Team = () => {

  const itemSize : number = 300;


  return (
    <div className='pt-10 px-[2rem] sm:px-[10rem]'>
        <div className="flex items-center justify-center">
            <p className="text-5xl">Team</p>
        </div>

        <div className="my-5 flex items-center justify-center ">
          <p className="text-2xl">With over 10+ years of combined experience in building, meet the team behind CNotes</p>
        </div>

        <div className="flex flex-row items-center justify-center">
          <div className="flex">
            <Image src={assets.jason_picture} alt="Jason Picture" width={itemSize/1.3}/>
          </div>
          <div className="flex">
            <Image src={assets.sean_picture} alt="Sean Picture" width={itemSize}/>
          </div>
          <div className="flex">
            <Image src={assets.unknown_picture} alt="Jason Picture" width={itemSize}/>
          </div>
          <div className="flex">
            <Image src={assets.unknown_picture} alt="Jason Picture" width={itemSize}/>
          </div>
        </div>
    </div>
  )
}

export default Team
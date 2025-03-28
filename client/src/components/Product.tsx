import React from 'react'
import {assets} from "../assets/asset.js";
import Image from 'next/image';
import "./Product.css"
const Product = () => {
  const itemSize : number = 1700;
  return (
    <div id="product" className='bg-gradient-to-b from-black via-violet-900 to-black py-20 px-[2rem] sm:px-[10rem] text-slate-100'>
        <div className="mb-10 flex items-center justify-center">
            <p className="text-5xl ">Features</p>
        </div>

        <div className="flex flex-col max-h-full mb-20">
          <div className="flex flex-col sm:flex-row ">
            <div id="notes-upload" className="flex border-4 border-amber-100 mb-10 sm:mb-0 w-full">
              <Image src={assets.notes_logo} alt="Notes Logo" width={itemSize}/>
            </div>

            <div className=" flex flex-col items-center justify-between text-center text-4xl text-wrap mx-10 sm:w-full">
              <p className="flex items-center mb-10 mt-20">Upload Your Notes In Any Format</p>
              <p className="text-2xl flex text-center ">CNotes is the ultimate tool for seamless note-taking and real-time collaboration. Create, edit, and share notes instantly with others. </p>
              <p className=""></p>
            </div>
          </div>
        </div>

        <div className="flex flex-col max-h-full mb-10">
          <div className="flex flex-col sm:flex-row-reverse ">
            <div id="ai-brain" className="flex border-4 border-amber-100 mb-10 sm:mb-0 w-full">
              <Image src={assets.ai_brain} alt="Notes Logo" width={itemSize}/>
            </div>

            <div className=" flex flex-col items-center justify-between text-center text-4xl text-wrap mx-10 sm:w-full">
              <p className="flex mb-10 mt-20">Collaboration with Teachers and Students</p>
              <p className="text-2xl  flex text-center">Our built-in discussion board allows you to dive deeper into ideas, ask questions, share insights, and discuss specific topics, making it easy to enhance your notes and collaborate effectively.</p>
              <p className=""></p>
            </div>
          </div>
        </div>

        <div className="flex flex-col max-h-full mb-10">
          <div className="flex flex-col sm:flex-row ">
            <div id="more-features" className="flex border-4 border-amber-100 mb-10 sm:mb-0 w-full">
              <Image src={assets.more_coming_soon} alt="Notes Logo" width={itemSize}/>
            </div>

            <div className=" flex flex-col items-center justify-between text-center text-4xl text-wrap mx-10 sm:w-full">
              <p className="flex">Stay Tuned, More Exciting Features Upcoming!</p>
              <p className="text-2xl  flex text-center">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eum officia inventore laudantium ut animi, facilis consequatur asperiores. Odio dolore hic asperiores facere. Nemo culpa maiores provident ullam assumenda quia unde!</p>
              <p className=""></p>
            </div>
          </div>
        </div>

        
    </div>
  )
}

export default Product
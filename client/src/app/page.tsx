import Hero from "@/components/homeComponents/Hero";
import Navbar from "@/components/homeComponents/Navbar";
import Image from "next/image";
import "../components/homeComponents/Hero.css"
import Product from "@/components/homeComponents/Product";
import Team from "@/components/homeComponents/Team";
export default function Home() {
  return (
    <div className="">
      <div id="gradient" className="h-full p-[2rem] pb-20 ">
        <Navbar />
        <Hero />
      </div>
      <div className="">
        <Team />
        <Product />
      </div>
      
    </div>
  );
}

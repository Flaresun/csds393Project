"use client";
import Hero from "@/components/Hero";
import Navbar from "@/components/Navbar";
import Image from "next/image";
import "../components/Hero.css"
import Product from "@/components/Product";
import Team from "@/components/Team";
import Customers from "@/components/Customers";
import Footer from "@/components/Footer";
<<<<<<< HEAD
import { useContext, useEffect } from "react";
import { AppContent } from "@/context/AppContext";
import { useRouter } from 'next/navigation'

export default function Home() {
  const {isAuth} = useContext<any>(AppContent);
    const router = useRouter();
  
  useEffect(() => {
    if (isAuth) {
      router.push("/dashboard");
    }
  },[isAuth])
=======
import { AppContent } from "@/context/AppContext";
import { useContext,useEffect} from "react";
import {useRouter} from "next/navigation";
export default function Home() {
  const {isAuth} = useContext<any>(AppContent);
  const router = useRouter();
  useEffect(() => {
    isAuth && router.push("/dashboard")
  })
>>>>>>> 58d9416417b5ce668b8d324107dc89bb67e7d2a8
  return (
    <div className="">
      <div id="gradient" className="h-full p-[2rem]">
        <Navbar />
        <Hero />
      </div>
      <div className="">
        <Team />
        <Product />
        <Customers />
        <Footer />
      </div>
      
    </div>
  );
}

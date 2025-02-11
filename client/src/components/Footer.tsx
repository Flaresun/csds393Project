import React from 'react';
import { FaGithub , FaTwitter, FaInstagram, FaLinkedin } from 'react-icons/fa';
import {assets} from "../assets/asset.js";
import Image from 'next/image';
const Footer = () => {
  return (
    <footer id="footer" className="bg-black text-white py-8 px-6">
      <div className="max-w-6xl mx-auto grid md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-6 text-center md:text-left">
        {/* Logo & Description */}
        <div>
          <Image src={assets.logo} alt="Logo" width={150}/>
          <p className="text-gray-400 mt-2">Your go-to platform for organizing and sharing notes effortlessly.</p>
        </div>

        {/* Quick Links */}
        <div>
          <h3 className="text-xl font-semibold">Quick Links</h3>
          <ul className="mt-2 space-y-2">
            <li><a href="#hero" className="text-gray-400 hover:text-violet-400">Home</a></li>
            <li><a href="#team" className="text-gray-400 hover:text-violet-400">Team</a></li>
            <li><a href="#product" className="text-gray-400 hover:text-violet-400">Product</a></li>
            <li><a href="#customers" className="text-gray-400 hover:text-violet-400">Customers</a></li>
          </ul>
        </div>

        {/* Social Media */}
        <div>
          <h3 className="text-xl font-semibold">Follow Us</h3>
          <div className="flex justify-center md:justify-start mt-3 space-x-4">
            <a href="https://github.com/Flaresun" className="text-gray-400 hover:text-violet-400"><FaGithub  size={24} /></a>
            <a href="#" className="text-gray-400 hover:text-violet-400"><FaTwitter size={24} /></a>
            <a href="#" className="text-gray-400 hover:text-violet-400"><FaInstagram size={24} /></a>
            <a href="#https://www.linkedin.com/in/seth-omeike-1a2681260/" className="text-gray-400 hover:text-violet-400"><FaLinkedin size={24} /></a>
          </div>
        </div>
      </div>

      {/* Copyright */}
      <div className="text-center text-gray-500 text-sm mt-6 border-t border-gray-700 pt-4">
        &copy; {new Date().getFullYear()} Cnotes. All rights reserved.
      </div>
    </footer>
  );
};

export default Footer;

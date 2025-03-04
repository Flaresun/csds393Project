"use client"

import { useState } from "react";
import ImageUpload from "./fileupload";

function Uploader() {
  const [imageUrl, setImageUrl] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!imageUrl) return;
    
    setIsSubmitting(true);
    // Simulate submission process
    setTimeout(() => {
      alert("Image submitted successfully!");
      setIsSubmitting(false);
    }, 1000);
  };

  return (
    <div className="max-w-7xl mx-auto flex justify-center items-start min-h-screen p-4 md:p-6">
      <div className="w-full max-w-3xl">
        <h1 className="text-gray-800 text-center font-bold text-2xl sm:text-3xl md:text-4xl pb-4 md:pb-6">
          Upload Image
        </h1>

        <div className="bg-white rounded-lg shadow-md p-4 md:p-6">
          <form onSubmit={handleSubmit}>
            <ImageUpload setImageUrl={setImageUrl} imageUrl={imageUrl} />

            
              <div className="mt-8 md:mt-12 w-full">
                
                <div className="mt-6 md:mt-8 flex justify-center">
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className={`px-6 py-3 rounded-lg text-white font-medium text-base md:text-lg transition-colors ${
                      isSubmitting 
                        ? "bg-blue-400 cursor-not-allowed" 
                        : "bg-blue-600 hover:bg-blue-700"
                    }`}
                  >
                    {isSubmitting ? "Submitting..." : "Submit Image"}
                  </button>
                </div>
              </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Uploader;
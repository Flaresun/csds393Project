import React from 'react';

const testimonials = [
  { name: 'Alice', title: 'Professor', message: 'This platform has been a game changer for my students!' },
  { name: 'Bob', title: 'Student', message: 'I love how easy it is to find and organize my notes.' },
  { name: 'Charlie', title: 'Parent', message: 'A fantastic resource that helps my child stay ahead in class.' },
  { name: 'David', title: 'Guardian', message: 'A well-structured platform that enhances learning experiences.' },
  { name: 'Eve', title: 'Professor', message: 'A must-have tool for modern education.' },
  { name: 'Frank', title: 'Student', message: 'Makes studying so much more efficient and fun!' },
  { name: 'Grace', title: 'Parent', message: 'I feel more involved in my child’s education with this tool.' },
  { name: 'Hannah', title: 'Guardian', message: 'Reliable and easy to use for all ages.' },
  { name: 'Ian', title: 'Professor', message: 'A well-designed system that keeps everything organized.' },
  { name: 'Jack', title: 'Student', message: 'I can finally keep track of my notes in one place!' },
  { name: 'Karen', title: 'Parent', message: 'A trustworthy platform that delivers results.' },
  { name: 'Leo', title: 'Guardian', message: 'User-friendly and highly recommended.' }
];

const Customers = () => {
  return (
    <div id="customers" className="bg-gradient-to-b from-black via-violet-900 to-black text-white py-12 px-6">
      <h2 className="text-3xl font-bold text-center mb-8">What Our Users Say</h2>
      <div className="grid md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-6 max-w-6xl mx-auto">
        {testimonials.map((testimonial, index) => (
          <div key={index} className="bg-gray-800 p-6 rounded-xl shadow-lg flex flex-col items-center text-center">
            <div className="w-12 h-12 flex items-center justify-center bg-blue-500 text-white text-lg font-bold rounded-full mb-4">
              {testimonial.name[0]}
            </div>
            <h3 className="text-xl font-semibold">{testimonial.name}</h3>
            <p className="text-sm text-gray-400 mb-2">{testimonial.title}</p>
            <p className="text-gray-300">"{testimonial.message}"</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Customers;

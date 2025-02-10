"use client";
import { useState } from "react";
import { LuEyeClosed } from "react-icons/lu";
import { RxEyeOpen } from "react-icons/rx";
import "../../components/Hero.css"; // Assuming this file exists for custom styles

const AuthPage = () => {
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [formType, setFormType] = useState<"login" | "signup">("login"); // Toggle between login and signup
  const [role, setRole] = useState<string>(""); // State for the role dropdown
  const [email, setEmail] = useState<string>(""); // State for the role dropdown
  const [password, setPassword] = useState<string>(""); // State for the role dropdown

  // Toggle password visibility
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  // Handle role change (for sign-up form)
  const handleRoleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setRole(e.target.value);
  };

  const handleSubmit = (e : any) : any => {
    e.preventDefault();
    console.log(role,email,password, formType)
  }

  return (
    <div id="gradient" className="flex justify-center items-center min-h-screen bg-black text-white">
      <div className="w-full max-w-md p-8 bg-gray-800 bg-opacity-50 rounded-lg">
        <h2 className="text-3xl font-semibold mb-6 text-center">
          {formType === "login" ? "Login" : "Sign Up"}
        </h2>

        <form>
          {/* Email Input */}
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm mb-2">Email</label>
            <input
              type="email"
              onChange={e => setEmail(e.target.value)} value={email} 
              className="w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg"
              placeholder="Enter your email"
              required
            />
          </div>

          {/* Password Input */}
          <div className="mb-4">
            <label htmlFor="password" className="block text-sm mb-2">Password</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                onChange={e => setPassword(e.target.value)} value={password} 
                className="w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg"
                placeholder="Enter your password"
                required
              />
              <span
                onClick={togglePasswordVisibility}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer"
              >
                {showPassword ? <RxEyeOpen className="text-gray-400" /> : <LuEyeClosed className="text-gray-400" />}
              </span>
            </div>
          </div>

          {/* Role Dropdown (For Sign Up only) */}
          {formType === "signup" && (
            <div className="mb-4">
              <label htmlFor="role" className="block text-sm mb-2">Role</label>
              <select
                id="role"
                value={role}
                onChange={handleRoleChange}
                className="w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg"
                required
              >
                <option value="Student">Student</option>
                <option value="Teacher">Teacher</option>
                <option value="Admin">Admin</option>
              </select>
            </div>
          )}

          {/* Submit Button */}
          <button
            onClick={handleSubmit} 
            className="w-full py-3 bg-blue-600 text-white rounded-lg mt-6"
          >
            {formType === "login" ? "Login" : "Sign Up"}
          </button>
        </form>

        {/* Toggle between Login and Sign Up */}
        <div className="text-center mt-4">
          {formType === "login" ? (
            <p>
              Don't have an account?{" "}
              <span
                onClick={() => setFormType("signup")}
                className="text-blue-400 cursor-pointer underline"
              >
                Sign Up
              </span>
            </p>
          ) : (
            <p>
              Already have an account?{" "}
              <span
                onClick={() => setFormType("login")}
                className="text-blue-400 cursor-pointer underline"
              >
                Login
              </span>
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthPage;


import React from "react";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-[#1a1d25] text-white shadow-md w-full absolute top-0">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        {/* Logo o título */}
        <div className="text-xl font-semibold">Residual Dense CNN</div>

        {/* Links de navegación */}
        <div className="flex space-x-6">
          <NavLink
            to="/tryit"
            className={({ isActive }) =>
              `text-lg font-medium ${
                isActive ? "text-[#4ade80] border-b-2 border-[#4ade80]" : "hover:text-gray-300"
              }`
            }
          >
            Try It
          </NavLink>
          <NavLink
            to="/"
            className={({ isActive }) =>
              `text-lg font-medium ${
                isActive ? "text-[#4ade80] border-b-2 border-[#4ade80]" : "hover:text-gray-300"
              }`
            }
          >
            Info
          </NavLink>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
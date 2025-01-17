import { useState } from "react";
import { NavLink } from "react-router-dom";

const TabBar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const tabs = [
    { name: "Home", path: "/" },
    { name: "Upload", path: "/upload" },
    { name: "Documents", path: "/documents" },
  ];

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <div className="bg-gray-900 text-white">
      <div className="container mx-auto flex justify-between items-center p-4">
        {/* Brand Logo */}
        <div className="text-2xl font-bold">Researchify</div>

        {/* Hamburger Menu Icon */}
        <button
          className="block md:hidden text-gray-300 hover:text-white focus:outline-none"
          onClick={toggleMenu}
        >
          {isMenuOpen ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16m-7 6h7"
              />
            </svg>
          )}
        </button>

        {/* Navigation Tabs */}
        <div
          className={`${
            isMenuOpen ? "block" : "hidden"
          } md:flex md:items-center absolute md:static top-16 left-0 w-full md:w-auto bg-gray-800 md:bg-transparent shadow-md md:shadow-none z-10`}
        >
          <ul className="flex flex-col md:flex-row md:space-x-6">
            {tabs.map((tab) => (
              <li key={tab.name} className="md:ml-4">
                <NavLink
                  to={tab.path}
                  className={({ isActive }) =>
                    `block px-4 py-2 rounded-lg md:inline ${
                      isActive
                        ? "bg-blue-500 text-white"
                        : "text-gray-300 hover:bg-gray-700 hover:text-white"
                    }`
                  }
                >
                  {tab.name}
                </NavLink>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TabBar;

import React from "react";

const Sidebar = () => {
  return (
    <nav className='hidden lg:flex flex-col w-64 h-screen bg-white border-r border-neutral-200'>
      <div className='p-4 border-b'>
        <div className='text-xl font-bold text-gray-800 cursor-pointer'>CoinSignals</div>
      </div>
      <div className='flex-1 overflow-y-auto'>
        <div className='p-4 space-y-2'>
          {/* Navigation Links */}
          {["Dashboard", "Analyzer", "DEX", "Social", "Signals", "Risk", "History"].map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase()}`}
              className='flex items-center px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg'>
              <span>{item}</span>
            </a>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Sidebar;

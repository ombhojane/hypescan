import React from "react";
// import Sidebar from "./components/Sidebar";
// import Header from "./components/Header";
import Dashboard from "./components/Dashboard";

function App() {
  return (
    <div className='flex'>
      {/* <Sidebar /> */}
      <div className='flex-1 ml-0 min-h-screen'>
        {/* <Header /> */}
        <Dashboard />
      </div>
    </div>
  );
}

export default App;

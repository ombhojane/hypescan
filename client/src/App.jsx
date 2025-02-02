import React from "react";
// import Sidebar from "./components/Sidebar";
// import Header from "./components/Header";
import Dashboard from "./components/Dashboard";

function App() {
  return (
    <div className='flex flex-col'>
      {/* <Sidebar /> */}
      <div className="flex">
        <img src="https://devfolio.co/_next/image?url=https%3A%2F%2Fassets.devfolio.co%2Fhackathons%2F06a691c532544f2b873e52e8c938e285%2Fprojects%2Fc2196ca8564a4a4f8d2d4b4e9843c6b2%2F7f08fd1d-77fd-4a66-b4f3-3fcf805df291.jpeg&w=1440&q=75" alt="" />
        <div>
          <h3>Hype Scan AI
          </h3>
          <p>Predict Meme Coin Pumps Before They Happen</p>
        </div>
      </div>
      <div className='flex-1 ml-0 min-h-screen'>
        {/* <Header /> */}
        <Dashboard />
      </div>
    </div>
  );
}

export default App;

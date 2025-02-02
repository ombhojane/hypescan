import React, { useState, useEffect } from "react";
import RiskAssessment from "./RiskAssessment";
import Historical from "./Historical";
import AISignals from "./AISignals";
import DexAnalytics from "./DexAnalytics";

const Dashboard = () => {
  const [loading, setLoading] = useState(false);
  const [coinData, setCoinData] = useState({
    id: "coin-123",
    networks: ["Ethereum", "BSC", "Polygon"],
    marketCap: 123456789,
    marketCapChange: 0.05,
    volume24h: 987654321,
    volume24hChange: 0.02,
    liquidity: 543210,
    liquidityChange: 0.01,
    honeypotRisk: 0.2,
    rugpullRisk: 0.6,
    washTrading: 0.1,
  });

  const [coinName, setCoinName] = useState("");
  const [network, setNetwork] = useState("");
  const [coinAddress, setCoinAddress] = useState(""); // New state for coin address
  const [pairAddress, setPairAddress] = useState(""); // New state for pair address

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Show loading state while the request is in progress

    try {
      // Construct the query parameters from the form state
      const queryParams = new URLSearchParams({
        coinAddress,
        pairAddress,
        // coinName,
        // network,
      }).toString();

      // Send the request with query params in the URL
      const response = await fetch(`/api/submit?${queryParams}`, {
        method: "GET", // Use GET method to send query params
      });

      const result = await response.json();
      // Assuming the response contains the updated coinData
      setCoinData(result); // Update the coinData state with the new data from the API
      setLoading(false); // Hide loading state after response
    } catch (error) {
      console.error("Error submitting the data:", error);
      setLoading(false); // Hide loading state in case of error
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!coinData) {
    return <div>No data found.</div>;
  }

  return (
    <main className='flex-1 ml-0 min-h-screen' id='el-flpsdfm3'>
      <div
        id={coinData.id}
        data-section_id={coinData.id}
        className='page_sectionHighlight__ahPeD sectionCode'>
        <htmlcode>
          <section id='coin-analyzer' className='p-6 bg-white'>
            <div className='grid grid-cols-1 lg:grid-cols-3 gap-6'>
              <div className='lg:col-span-1 space-y-6'>
                <div className='p-4 border border-neutral-200/20 rounded-lg'>
                  <h3 className='text-lg font-semibold mb-4'>Coin Analysis Input</h3>
                  <form onSubmit={handleSubmit} className='space-y-4'>
                    {/* <div>
                      <label
                        className='block text-sm font-medium text-gray-700 mb-1'
                        htmlFor='coin-name'>
                        Coin Name/Symbol
                      </label>
                      <input
                        type='text'
                        id='coin-name'
                        value={coinName}
                        onChange={(e) => setCoinName(e.target.value)}
                        className='w-full p-2 border border-neutral-200/30 rounded-lg focus:ring-2 focus:ring-blue-500/50'
                        placeholder='Enter coin name or symbol'
                      />
                    </div>
                    <div>
                      <label
                        className='block text-sm font-medium text-gray-700 mb-1'
                        htmlFor='network'>
                        Network
                      </label>
                      <select
                        id='network'
                        value={network}
                        onChange={(e) => setNetwork(e.target.value)}
                        className='w-full p-2 border border-neutral-200/30 rounded-lg'>
                        {coinData.networks.map((networkOption) => (
                          <option key={networkOption} value={networkOption}>
                            {networkOption}
                          </option>
                        ))}
                      </select>
                    </div> */}
                    <div>
                      <label
                        className='block text-sm font-medium text-gray-700 mb-1'
                        htmlFor='coin-address'>
                        Coin Address
                      </label>
                      <input
                        type='text'
                        id='coin-address'
                        value={coinAddress}
                        onChange={(e) => setCoinAddress(e.target.value)}
                        className='w-full p-2 border border-neutral-200/30 rounded-lg focus:ring-2 focus:ring-blue-500/50'
                        placeholder='Enter coin address'
                      />
                    </div>
                    <div>
                      <label
                        className='block text-sm font-medium text-gray-700 mb-1'
                        htmlFor='pair-address'>
                        Pair Address
                      </label>
                      <input
                        type='text'
                        id='pair-address'
                        value={pairAddress}
                        onChange={(e) => setPairAddress(e.target.value)}
                        className='w-full p-2 border border-neutral-200/30 rounded-lg focus:ring-2 focus:ring-blue-500/50'
                        placeholder='Enter pair address'
                      />
                    </div>
                    <button
                      type='submit'
                      className='w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors'>
                      Analyze Coin
                    </button>
                  </form>
                </div>
              </div>

              <div className='lg:col-span-2 space-y-6'>
                <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
                  <div className='p-4 border border-neutral-200/20 rounded-lg'>
                    <div className='text-sm text-gray-500'>Market Cap</div>
                    <div className='text-xl font-semibold'>${coinData.marketCap}</div>
                    <div
                      className={`text-sm ${
                        coinData.marketCapChange > 0 ? "text-green-500" : "text-red-500"
                      }`}>
                      {coinData.marketCapChange > 0 ? "+" : "-"}
                      {(coinData.marketCapChange * 100).toFixed(2)}%
                    </div>
                  </div>
                  <div className='p-4 border border-neutral-200/20 rounded-lg'>
                    <div className='text-sm text-gray-500'>24h Volume</div>
                    <div className='text-xl font-semibold'>${coinData.volume24h}</div>
                    <div
                      className={`text-sm ${
                        coinData.volume24hChange > 0 ? "text-green-500" : "text-red-500"
                      }`}>
                      {coinData.volume24hChange > 0 ? "+" : "-"}
                      {(coinData.volume24hChange * 100).toFixed(2)}%
                    </div>
                  </div>
                  <div className='p-4 border border-neutral-200/20 rounded-lg'>
                    <div className='text-sm text-gray-500'>Liquidity</div>
                    <div className='text-xl font-semibold'>${coinData.liquidity}</div>
                    <div
                      className={`text-sm ${
                        coinData.liquidityChange > 0 ? "text-green-500" : "text-red-500"
                      }`}>
                      {coinData.liquidityChange > 0 ? "+" : "-"}
                      {(coinData.liquidityChange * 100).toFixed(2)}%
                    </div>
                  </div>
                </div>

                <div className='p-4 border border-neutral-200/20 rounded-lg'>
                  <h3 className='text-lg font-semibold mb-4'>Risk Assessment</h3>
                  <div className='space-y-3'>
                    <div className='flex items-center'>
                      <div className='w-32 text-sm text-gray-600'>Honeypot Risk:</div>
                      <div className='flex-1'>
                        <div className='w-full h-2 bg-gray-200 rounded-full'>
                          <div
                            className={`w-[${coinData.honeypotRisk * 100}%] h-2 bg-${
                              coinData.honeypotRisk > 0.5 ? "red-500" : "green-500"
                            } rounded-full`}
                          />
                        </div>
                      </div>
                      <div
                        className={`ml-4 text-sm text-${
                          coinData.honeypotRisk > 0.5 ? "red-600" : "green-600"
                        }`}>
                        {coinData.honeypotRisk > 0.5 ? "High" : "Low"}
                      </div>
                    </div>
                    <div className='flex items-center'>
                      <div className='w-32 text-sm text-gray-600'>Rugpull Risk:</div>
                      <div className='flex-1'>
                        <div className='w-full h-2 bg-gray-200 rounded-full'>
                          <div
                            className={`w-[${coinData.rugpullRisk * 100}%] h-2 bg-${
                              coinData.rugpullRisk > 0.5 ? "red-500" : "green-500"
                            } rounded-full`}
                          />
                        </div>
                      </div>
                      <div
                        className={`ml-4 text-sm text-${
                          coinData.rugpullRisk > 0.5 ? "red-600" : "green-600"
                        }`}>
                        {coinData.rugpullRisk > 0.5 ? "High" : "Low"}
                      </div>
                    </div>
                    <div className='flex items-center'>
                      <div className='w-32 text-sm text-gray-600'>Wash Trading:</div>
                      <div className='flex-1'>
                        <div className='w-full h-2 bg-gray-200 rounded-full'>
                          <div
                            className={`w-[${coinData.washTrading * 100}%] h-2 bg-${
                              coinData.washTrading > 0.5 ? "red-500" : "green-500"
                            } rounded-full`}
                          />
                        </div>
                      </div>
                      <div
                        className={`ml-4 text-sm text-${
                          coinData.washTrading > 0.5 ? "red-600" : "green-600"
                        }`}>
                        {coinData.washTrading > 0.5 ? "High" : "Low"}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </htmlcode>
      </div>

      {/* Pass the coin address and pair address as props */}
      <DexAnalytics coinAddress={coinAddress} pairAddress={pairAddress} />
      <AISignals coinAddress={coinAddress} pairAddress={pairAddress} />
      <RiskAssessment coinAddress={coinAddress} pairAddress={pairAddress} />
      <Historical coinAddress={coinAddress} pairAddress={pairAddress} />
    </main>
  );
};

export default Dashboard;

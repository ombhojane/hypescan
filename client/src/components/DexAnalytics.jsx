import React, { useState, useEffect } from "react";

const DexAnalytics = ({ coinAddress, pairAddress }) => {
  // Step 1: Create state variables for storing data
  const [data, setData] = useState({
    total_dex_volume: 1234567890,
    dex_volume_change: 15.2,
    total_liquidity: 234567890,
    liquidity_change: -3.5,
    unique_traders: 890123,
    traders_change: 5.4,
    liquidity_pool: [
      {
        platform: "Uniswap",
        pair: "ETH/USDT",
        liquidity: 50,
        change: 12.5,
      },
      {
        platform: "SushiSwap",
        pair: "BTC/USDT",
        liquidity: 30,
        change: -5.2,
      },
    ],
    whale_transactions: [
      {
        address: "0x12345...",
        amount: 500,
        asset: "ETH",
        time_ago: "5 minutes ago",
      },
      {
        address: "0x67890...",
        amount: -250,
        asset: "BTC",
        time_ago: "1 hour ago",
      },
    ],
  });

  // Step 2: Fetch data from the API when the component mounts
  useEffect(() => {
    const fetchData = async () => {
      try {
        const url = new URL("https://hypescan.onrender.com/dex-analytics");
        const params = {
          coinAddress, // Adding the coinAddress as a query parameter
          pairAddress, // Adding the pairAddress as a query parameter
        };
        url.search = new URLSearchParams(params).toString();

        const response = await fetch(url);
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error("Error fetching DEX analytics data: ", error);
      }
    };

    // Only fetch data if both coinAddress and pairAddress are provided
    if (coinAddress && pairAddress) {
      fetchData();
    }
  }, [coinAddress, pairAddress]); // The effect runs when either coinAddress or pairAddress changes

  // Step 3: Show loading state until data is fetched
  if (!data || !coinAddress || !pairAddress) {
    return <div>Loading...</div>; // Or a spinner or other loading indication
  }

  return (
    <div
      id='cf09cb5d-9233-4bcd-a25b-9b1c351d45e6'
      className='page_sectionHighlight__ahPeD sectionCode'>
      <section id='dex-analytics' className='p-6 bg-white'>
        {/* DEX Analytics Overview */}
        <div className='grid grid-cols-1 md:grid-cols-3 gap-6 mb-6'>
          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Total DEX Volume (24h)</h3>
            <div className='text-2xl font-semibold mt-2'>
              ${data.total_dex_volume.toLocaleString()}
            </div>
            <div className='flex items-center mt-2 text-green-500 text-sm'>
              <span>↑ {data.dex_volume_change}%</span>
            </div>
          </div>

          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Total Liquidity</h3>
            <div className='text-2xl font-semibold mt-2'>
              ${data.total_liquidity.toLocaleString()}
            </div>
            <div className='flex items-center mt-2 text-red-500 text-sm'>
              <span>↓ {data.liquidity_change}%</span>
            </div>
          </div>

          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Unique Traders</h3>
            <div className='text-2xl font-semibold mt-2'>{data.unique_traders}</div>
            <div className='flex items-center mt-2 text-green-500 text-sm'>
              <span>↑ {data.traders_change}%</span>
            </div>
          </div>
        </div>

        {/* Liquidity Pool Analysis */}
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
          {data.liquidity_pool.map((pool, index) => (
            <div className='border border-neutral-200/20 rounded-lg p-4' key={index}>
              <h3 className='text-lg font-semibold mb-4'>Liquidity Pool Analysis</h3>
              <div className='space-y-4'>
                <div className='flex justify-between items-center p-3 bg-gray-50 rounded'>
                  <div>
                    <div className='font-medium'>{pool.platform}</div>
                    <div className='text-sm text-gray-500'>{pool.pair}</div>
                  </div>
                  <div className='text-right'>
                    <div className='font-medium'>${pool.liquidity}M</div>
                    <div className={`text-${pool.change > 0 ? "green" : "red"}-500`}>
                      {pool.change > 0 ? `+${pool.change}%` : `-${Math.abs(pool.change)}%`}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Whale Transactions */}
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
          {data.whale_transactions.map((transaction, index) => (
            <div className='border border-neutral-200/20 rounded-lg p-4' key={index}>
              <h3 className='text-lg font-semibold mb-4'>Whale Transactions</h3>
              <div className='flex items-center justify-between p-3 bg-gray-50 rounded'>
                <div className='flex items-center'>
                  <div
                    className={`w-2 h-2 bg-${
                      transaction.amount > 0 ? "green" : "red"
                    }-500 rounded-full mr-2`}
                  />
                  <div className='text-sm font-medium'>{transaction.address}</div>
                </div>
                <div className='text-sm'>
                  {transaction.amount} {transaction.asset}
                </div>
                <div className='text-sm text-gray-500'>{transaction.time_ago}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Add more dynamic sections as needed */}
      </section>
    </div>
  );
};

export default DexAnalytics;

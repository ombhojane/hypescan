import React, { useState, useEffect } from "react";

const Historical = ({ coinAddress, pairAddress }) => {
  // Step 1: Create state variables to store API data
  const [historicalData, setHistoricalData] = useState({
    roi: 1245,
    pumpPatterns: 4,
    averagePumpReturn: 85,
    recoveryTime: 48,
  });
  const [alertsData, setAlertsData] = useState({
    activeAlerts: 24,
    highPriority: 12,
    triggeredToday: 8,
    triggeredChange: 3,
    successRate: 92,
    responseTime: 1.2,
  });

  // Step 2: Fetch data from the API
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Constructing the API URLs with coinAddress and pairAddress as query parameters
        const historicalUrl = new URL("https://api.example.com/historical-analysis");
        const alertsUrl = new URL("https://api.example.com/alerts-notifications");

        // Add query parameters for coinAddress and pairAddress
        const params = { coinAddress, pairAddress };
        historicalUrl.search = new URLSearchParams(params).toString();
        alertsUrl.search = new URLSearchParams(params).toString();

        // Fetch data from the API
        const historicalResponse = await fetch(historicalUrl);
        const alertsResponse = await fetch(alertsUrl);

        // Parsing the JSON responses
        const historicalJson = await historicalResponse.json();
        const alertsJson = await alertsResponse.json();

        // Update the state with the fetched data
        setHistoricalData(historicalJson);
        setAlertsData(alertsJson);
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };

    // Only fetch data if both coinAddress and pairAddress are provided
    if (coinAddress && pairAddress) {
      fetchData();
    }
  }, [coinAddress, pairAddress]); // The effect runs when either coinAddress or pairAddress changes

  // Step 3: Render the dynamic data in the JSX
  if (!historicalData || !alertsData) {
    return <div>Loading...</div>; // Handle loading state
  }

  return (
    <div>
      {/* Historical Analysis Section */}
      <section id='historical-analysis' className='p-6 bg-white'>
        <div className='grid grid-cols-1 md:grid-cols-4 gap-6 mb-6'>
          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Historical ROI</h3>
            <div className='text-2xl font-semibold mt-2'>{historicalData.roi}%</div>
            <div className='flex items-center mt-2 text-gray-500 text-sm'>
              <span>Since Launch</span>
            </div>
          </div>

          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Pump Patterns</h3>
            <div className='text-2xl font-semibold mt-2'>
              {historicalData.pumpPatterns} Detected
            </div>
            <div className='flex items-center mt-2 text-gray-500 text-sm'>
              <span>Last 30 Days</span>
            </div>
          </div>

          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Average Pump Return</h3>
            <div className='text-2xl font-semibold mt-2'>{historicalData.averagePumpReturn}%</div>
            <div className='flex items-center mt-2 text-gray-500 text-sm'>
              <span>Per Event</span>
            </div>
          </div>

          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Recovery Time</h3>
            <div className='text-2xl font-semibold mt-2'>{historicalData.recoveryTime}h</div>
            <div className='flex items-center mt-2 text-gray-500 text-sm'>
              <span>Average</span>
            </div>
          </div>
        </div>
      </section>

      {/* Alerts & Notifications Section */}
      <section id='alerts-notifications' className='p-6 bg-white'>
        <div className='grid grid-cols-1 md:grid-cols-4 gap-6 mb-6'>
          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Active Alerts</h3>
            <div className='text-2xl font-semibold mt-2'>{alertsData.activeAlerts}</div>
            <div className='flex items-center mt-2 text-blue-500 text-sm'>
              <span>{alertsData.highPriority} High Priority</span>
            </div>
          </div>

          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Triggered Today</h3>
            <div className='text-2xl font-semibold mt-2'>{alertsData.triggeredToday}</div>
            <div className='flex items-center mt-2 text-green-500 text-sm'>
              <span>↑ {alertsData.triggeredChange} from yesterday</span>
            </div>
          </div>

          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Success Rate</h3>
            <div className='text-2xl font-semibold mt-2'>{alertsData.successRate}%</div>
            <div className='flex items-center mt-2 text-gray-500 text-sm'>
              <span>Last 30 days</span>
            </div>
          </div>

          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Response Time</h3>
            <div className='text-2xl font-semibold mt-2'>{alertsData.responseTime}s</div>
            <div className='flex items-center mt-2 text-green-500 text-sm'>
              <span>Avg. Delivery</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Historical;

import React, { useState, useEffect } from "react";
const AISignals = ({ coinAddress, pairAddress }) => {
  // Step 1: Create state variables to store API data
  const [aiSignals, setAiSignals] = useState({
    strength: "Strong Buy",
    confidence: 85,
    pattern: "Accumulation",
    patternPhase: "Phase 2/4",
    prediction: "+42% Expected",
    forecast: "24h Forecast",
  });
  const [featureEngineering, setFeatureEngineering] = useState([
    {
      name: "Social Volume Velocity",
      weight: 30,
      color: "green",
      value: 85,
    },
    {
      name: "Influencer Impact",
      weight: 20,
      color: "blue",
      value: 65,
    },
    {
      name: "Historical Pump Pattern",
      weight: 25,
      color: "purple",
      value: 75,
    },
  ]);
  const [blockchainRecognition, setBlockchainRecognition] = useState([
    {
      name: "Wash Trading Detection",
      timeFrame: "Last 24 Hours",
      riskColor: "green",
      riskLevel: "Low Risk",
      riskPercentage: 5,
    },
    {
      name: "Smart Money Movement",
      timeFrame: "Accumulation Phase",
      riskColor: "green",
      riskLevel: "Strong Signal",
      riskPercentage: 95,
    },
  ]);
  const [alertThresholds, setAlertThresholds] = useState([
    {
      name: "Social Mention Spike (+400% in 4h)",
      status: "Triggered",
      color: "green",
      bgColor: "green",
    },
    {
      name: "Liquidity Change (±15% in 24h)",
      status: "Warning",
      color: "yellow",
      bgColor: "yellow",
    },
    {
      name: "Transaction Volume (2x 7-day avg)",
      status: "Normal",
      color: "gray",
      bgColor: "gray",
    },
  ]);

  // Step 2: Fetch data from API using coinAddress and pairAddress
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Constructing the API URLs with coinAddress and pairAddress
        const aiSignalsUrl = new URL("https://hypescan.onrender.com/ai-signals");
        const featureEngineeringUrl = new URL("https://hypescan.onrender.com/feature-engineering");
        const blockchainRecognitionUrl = new URL("https://hypescan.onrender.com/blockchain-recognition");
        const alertThresholdsUrl = new URL("https://hypescan.onrender.com/alert-thresholds");

        // Add query parameters for coinAddress and pairAddress
        const params = {
          coinAddress,
          pairAddress,
        };

        aiSignalsUrl.search = new URLSearchParams(params).toString();
        featureEngineeringUrl.search = new URLSearchParams(params).toString();
        blockchainRecognitionUrl.search = new URLSearchParams(params).toString();
        alertThresholdsUrl.search = new URLSearchParams(params).toString();

        // Fetching data from API
        const aiSignalsResponse = await fetch(aiSignalsUrl);
        const featureEngineeringResponse = await fetch(featureEngineeringUrl);
        const blockchainRecognitionResponse = await fetch(blockchainRecognitionUrl);
        const alertThresholdsResponse = await fetch(alertThresholdsUrl);

        // Parsing the JSON responses
        const aiSignalsData = await aiSignalsResponse.json();
        const featureEngineeringData = await featureEngineeringResponse.json();
        const blockchainRecognitionData = await blockchainRecognitionResponse.json();
        const alertThresholdsData = await alertThresholdsResponse.json();

        // Setting state with the fetched data
        setAiSignals(aiSignalsData);
        setFeatureEngineering(featureEngineeringData);
        setBlockchainRecognition(blockchainRecognitionData);
        setAlertThresholds(alertThresholdsData);
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };

    // Only fetch data if both coinAddress and pairAddress are provided
    if (coinAddress && pairAddress) {
      fetchData();
    }
  }, [coinAddress, pairAddress]); // The effect runs when either coinAddress or pairAddress changes

  // Step 3: Render the dynamic data
  if (!aiSignals || !featureEngineering || !blockchainRecognition || !alertThresholds) {
    return <div>Loading...</div>; // Loading state
  }

  return (
    <div
      id='b4b20e92-52e4-45b6-ae07-0d7eb94e43cd'
      className='page_sectionHighlight__ahPeD sectionCode'>
      <section id='ai-signals' className='p-6 bg-white'>
        {/* AI Signals Overview */}
        <div className='grid grid-cols-1 md:grid-cols-3 gap-6 mb-6'>
          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Overall Signal Strength</h3>
            <div className='text-2xl font-semibold mt-2'>{aiSignals.strength}</div>
            <div className='flex items-center mt-2 text-green-500 text-sm'>
              <span>Confidence: {aiSignals.confidence}%</span>
            </div>
          </div>

          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Pattern Recognition</h3>
            <div className='text-2xl font-semibold mt-2'>{aiSignals.pattern}</div>
            <div className='flex items-center mt-2 text-blue-500 text-sm'>
              <span>{aiSignals.patternPhase}</span>
            </div>
          </div>

          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>AI Prediction</h3>
            <div className='text-2xl font-semibold mt-2'>{aiSignals.prediction}</div>
            <div className='flex items-center mt-2 text-gray-500 text-sm'>
              <span>{aiSignals.forecast}</span>
            </div>
          </div>
        </div>

        {/* Feature Engineering Matrix */}
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
          <div className='border border-neutral-200/20 rounded-lg p-4'>
            <h3 className='text-lg font-semibold mb-4'>Feature Engineering Matrix</h3>
            <div className='space-y-4'>
              {featureEngineering.map((feature) => (
                <div key={feature.name} className='space-y-2'>
                  <div className='flex justify-between text-sm'>
                    <span>{feature.name}</span>
                    <span className={`text-${feature.color}-500`}>{feature.weight}% Weight</span>
                  </div>
                  <div className='w-full h-2 bg-gray-200 rounded'>
                    <div
                      className={`w-[${feature.value}%] h-2 bg-${feature.color}-500 rounded`}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Blockchain Pattern Recognition */}
          <div className='border border-neutral-200/20 rounded-lg p-4'>
            <h3 className='text-lg font-semibold mb-4'>Blockchain Pattern Recognition</h3>
            <div className='space-y-4'>
              {blockchainRecognition.map((pattern) => (
                <div
                  key={pattern.name}
                  className='flex items-center justify-between p-3 bg-gray-50 rounded'>
                  <div>
                    <div className='font-medium'>{pattern.name}</div>
                    <div className='text-sm text-gray-500'>{pattern.timeFrame}</div>
                  </div>
                  <div className={`text-sm text-${pattern.riskColor}-500`}>
                    {pattern.riskLevel} ({pattern.riskPercentage}%)
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Alert Thresholds Status */}
        <div className='lg:col-span-2 border border-neutral-200/20 rounded-lg p-4'>
          <h3 className='text-lg font-semibold mb-4'>Alert Thresholds Status</h3>
          <div className='space-y-3'>
            {alertThresholds.map((alert) => (
              <div
                key={alert.name}
                className={`flex items-center justify-between p-3 bg-${alert.bgColor}-50 rounded`}>
                <span className='font-medium'>{alert.name}</span>
                <span className={`text-${alert.color}-500`}>{alert.status}</span>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default AISignals;

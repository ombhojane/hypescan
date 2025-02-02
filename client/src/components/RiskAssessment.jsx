import React, { useEffect, useState } from "react";

const RiskAssessment = ({ coinAddress, pairAddress }) => {
  const [data, setData] = useState({
    sectionId: "5a8714c4-1dbf-42ca-8baf-61526238d342",
    overallRiskScore: "Medium Risk",
    riskLevel: "6.5/10",
    smartContractSafetyPercentage: 85,
    smartContractStatus: "Audited & Verified",
    liquidityLockStatus: "Locked",
    liquidityLockRemainingDays: 180,
    ownershipStatus: "Renounced",
    ownershipStatusDescription: "Contract ownership has been renounced, reducing rugpull risk",
    mintFunctionStatus: "Present",
    mintFunctionDescription: "Contract contains mint function - potential supply inflation risk",
    transferRestrictions: "Limited",
    transferRestrictionsDescription: "Max transaction limit: 1% of total supply",
    liquidityRisk: "Medium",
    liquidityRiskPercentage: 45,
    concentrationRisk: "High",
    concentrationRiskPercentage: 75,
    smartContractRisk: "Low",
    smartContractRiskPercentage: 15,
  });

  // Fetch data from the API
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Constructing the API URL with coinAddress and pairAddress as query parameters
        const url = new URL("https://hypescan.onrender.com/risk-assessment");

        // Add query parameters for coinAddress and pairAddress
        const params = { coinAddress, pairAddress };
        url.search = new URLSearchParams(params).toString();

        // Fetch data from the API
        const response = await fetch(url);
        const result = await response.json();

        // Update the state with the fetched data
        setData(result);
      } catch (error) {
        console.error("Error fetching risk assessment data:", error);
      }
    };

    // Only fetch data if both coinAddress and pairAddress are provided
    if (coinAddress && pairAddress) {
      fetchData();
    }
  }, [coinAddress, pairAddress]); // The effect runs when either coinAddress or pairAddress changes

  // Show loading state if data is not available yet
  if (!data) {
    return <div>Loading...</div>;
  }

  return (
    <div
      id={data.sectionId}
      data-section_id={data.sectionId}
      className='page_sectionHighlight__ahPeD sectionCode'>
      <section id='risk-assessment' className='p-6 bg-white'>
        <div className='grid grid-cols-1 md:grid-cols-3 gap-6 mb-6'>
          {/* Overall Risk Score */}
          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Overall Risk Score</h3>
            <div className='text-2xl font-semibold mt-2'>{data.overallRiskScore}</div>
            <div className='flex items-center mt-2 text-yellow-500 text-sm'>
              <span>Risk Level: {data.riskLevel}</span>
            </div>
          </div>

          {/* Smart Contract Safety */}
          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Smart Contract Safety</h3>
            <div className='text-2xl font-semibold mt-2'>{data.smartContractSafetyPercentage}%</div>
            <div className='flex items-center mt-2 text-green-500 text-sm'>
              <span>{data.smartContractStatus}</span>
            </div>
          </div>

          {/* Liquidity Lock Status */}
          <div className='p-4 border border-neutral-200/20 rounded-lg'>
            <h3 className='text-sm text-gray-500'>Liquidity Lock Status</h3>
            <div className='text-2xl font-semibold mt-2'>{data.liquidityLockStatus}</div>
            <div className='flex items-center mt-2 text-blue-500 text-sm'>
              <span>{data.liquidityLockRemainingDays} Days Remaining</span>
            </div>
          </div>
        </div>

        {/* Other sections */}
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
          {/* Smart Contract Analysis */}
          <div className='border border-neutral-200/20 rounded-lg p-4'>
            <h3 className='text-lg font-semibold mb-4'>Smart Contract Analysis</h3>
            <div className='space-y-4'>
              {/* Ownership Status */}
              <div className='p-3 bg-gray-50 rounded'>
                <div className='flex justify-between mb-2'>
                  <span className='font-medium'>Ownership Status</span>
                  <span className='text-green-500'>{data.ownershipStatus}</span>
                </div>
                <div className='text-sm text-gray-500'>{data.ownershipStatusDescription}</div>
              </div>

              {/* Mint Function */}
              <div className='p-3 bg-gray-50 rounded'>
                <div className='flex justify-between mb-2'>
                  <span className='font-medium'>Mint Function</span>
                  <span
                    className={`text-${
                      data.mintFunctionStatus === "Present" ? "red" : "green"
                    }-500`}>
                    {data.mintFunctionStatus}
                  </span>
                </div>
                <div className='text-sm text-gray-500'>{data.mintFunctionDescription}</div>
              </div>

              {/* Transfer Restrictions */}
              <div className='p-3 bg-gray-50 rounded'>
                <div className='flex justify-between mb-2'>
                  <span className='font-medium'>Transfer Restrictions</span>
                  <span className='text-yellow-500'>{data.transferRestrictions}</span>
                </div>
                <div className='text-sm text-gray-500'>{data.transferRestrictionsDescription}</div>
              </div>
            </div>
          </div>

          {/* Risk Metrics */}
          <div className='border border-neutral-200/20 rounded-lg p-4'>
            <h3 className='text-lg font-semibold mb-4'>Risk Metrics</h3>
            <div className='space-y-4'>
              {/* Example of Liquidity Risk */}
              <div className='space-y-2'>
                <div className='flex justify-between text-sm'>
                  <span>Liquidity Risk</span>
                  <span className='text-yellow-500'>
                    {data.liquidityRisk} ({data.liquidityRiskPercentage}%)
                  </span>
                </div>
                <div className='w-full h-2 bg-gray-200 rounded'>
                  <div
                    className={`w-[${data.liquidityRiskPercentage}%] h-2 bg-yellow-500 rounded`}></div>
                </div>
              </div>

              {/* Example of Concentration Risk */}
              <div className='space-y-2'>
                <div className='flex justify-between text-sm'>
                  <span>Concentration Risk</span>
                  <span className='text-red-500'>
                    {data.concentrationRisk} ({data.concentrationRiskPercentage}%)
                  </span>
                </div>
                <div className='w-full h-2 bg-gray-200 rounded'>
                  <div
                    className={`w-[${data.concentrationRiskPercentage}%] h-2 bg-red-500 rounded`}></div>
                </div>
              </div>

              {/* Example of Smart Contract Risk */}
              <div className='space-y-2'>
                <div className='flex justify-between text-sm'>
                  <span>Smart Contract Risk</span>
                  <span className='text-green-500'>
                    {data.smartContractRisk} ({data.smartContractRiskPercentage}%)
                  </span>
                </div>
                <div className='w-full h-2 bg-gray-200 rounded'>
                  <div
                    className={`w-[${data.smartContractRiskPercentage}%] h-2 bg-green-500 rounded`}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default RiskAssessment;

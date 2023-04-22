import React, { useEffect, useState } from "react";
import 'regenerator-runtime/runtime'
import Chart from "chart.js/auto";
import { Line } from "react-chartjs-2";
import axios from "axios";

const country = document.getElementById('react').getAttribute('data-country');
const url = '/api/graph/?country=' + encodeURIComponent(country);

const fetchData = async (url) => {
    try {
        const {
            data: { count, country, date },
        } = await axios.get(url);
        const modifiedData = { count, country, date };
        console.log(modifiedData);
        return modifiedData;
    } catch (err) {
        console.log(err);
    }
};

const fetchDailyData = async () => {
    try {
        const { data } = await axios.get(url);
        console.log(data);
        return data;
    } catch (err) {
        console.log(err);
    }
};

const Graph = () => {
    const [dailyData, setDailyData] = useState([]);
  
    const fetchApi = async () => {
      const dailyData = await fetchDailyData();
      setDailyData(dailyData);
    };
  
    useEffect(() => {
      fetchApi();
    }, []);
  
    const lineChart = dailyData[0] ? (
        <Line
            data={{
                labels: dailyData.map(({ date }) =>
                    new Date(date).toLocaleDateString()
                ),
                datasets: [{
                    data: dailyData.map((data) => data.count),
                    label: "Daily Mentions",
                    backgroundColor: 'rgba(168, 200, 207, 0.8)',
                    borderColor: 'rgba(0,0,0,1)',
                    fill: true,
                }],
            }}
        />
    ) : null;
  
    return (
      <>
        <div>{lineChart}</div>
      </>
    );
  };
  
  export default Graph;
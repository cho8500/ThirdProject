/**
 * data.jsp에서 받아온 데이터를 각 js로 보내주는 스크립트
 */

let StackData = {
	categories : [],
	series : [
		{ name : "Stock Price",     data : [] },
		{ name : "Sentiment Score", data : [] }
	]
};

let stackData = [];

function filterStockData(stockName)
{
	let filteredData = allData.filter(item => item.name === stockName);
	
	// x축 데이터 설정
	chartData.categories = filteredData.map(item => item.date);
	
	// y축 데이터 설정
	chartData.series[0].data = filteredData.map(item => item.sise !== null ? parseInt(item.sise) : null);
	chartData.series[1].data = filteredData.map(item => parseInt(item.score));

	updateChart();
}

fetch("data.jsp")
	.then(response => response.json())
	.then(response => { StackData = response.StackData; })
	.catch(error => console.error("[Error] loading StackData : ", error));

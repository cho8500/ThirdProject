/**
 *  index.jsp 스크립트
 */

document.addEventListener("DOMContentLoaded", function () {

	//var stockData = [];
	if (stockData == null || stockData == undefined){
		const stockData = [];
	}
	
	fetch("data.jsp")
		.then(response => response.json())
		.then(data => {
			//console.log(data.stockNames)
			data.stockNames.forEach( item => stockData.push(item) );
			//stockData = data.stockNames;
			//console.log(stockData)
		})
		.catch(error => console.error("[Error] loading stockNames:", error));
});
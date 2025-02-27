/**
 *  index.jsp 스크립트
 */

document.addEventListener("DOMContentLoaded", function () {

	let stockData = [];
	
	fetch("data.jsp")
		.then(response => response.json())
		.then(data => {
			stockData = data.stockNames;
			console.log(stockData)
		})
		.catch(error => console.error("[Error] loading stockNames:", error));
});
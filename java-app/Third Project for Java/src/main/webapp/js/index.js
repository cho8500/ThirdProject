/**
 *  index 스크립트
 */

let stockData = [];

document.addEventListener("DOMContentLoaded", function () {
	
	fetch("data.jsp")
		.then(response => response.json())
		.then(data => {
			stockData = data.stockNames;
			console.log(stockData)
		})
		.catch(error => console.error("[Error] loading stockNames:", error));
});
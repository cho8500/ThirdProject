/**
 *  index 스크립트
 */

console.log("[stockData] ", stockData);

/* 자동완성 */
function autoComplete() {
	
	let query = document.querySelector("#query").value.trim();
	let list  = document.querySelector("#autocomplete_list");
	
	console.log("[query] ", query);
	console.log("[list] ", list);
	
	list.innerHTML     = "";
	list.style.display = "none";
	
	if(query.length === 0) { return; }
	
	let filteredStocks = stockData.filter(stock => 
		stock.name.includes(query) || stock.code.includes(query)
	);
	
	console.log("[filteredStocks] ", filteredStocks);
	
	if(filteredStocks.length > 0) {
		
		list.style.display = "block";
		
		filteredStocks.forEach(stock => {
			let item       = document.createElement("div");
			item.innerHTML = `${stock.name} (${stock.code})`;
			
			console.log("[item.innerHTML] ", item.innerHTML);
			
			item.onclick = function() {
				document.querySelector("#query").value = stock.name;
				list.style.display = "none";
			};
			list.appendChild(item);
		});
		list.classList.add("show");
	}
}

function hideAutoComplete() {
	
	setTimeout(() => {
		document.querySelector("#autocomplete_list").style.display = "none";
	}, 200);
}
/**
 * result.jsp 스크립트
 */

/* window onload */
document.addEventListener("DOMContentLoaded", function() {
	
	let query = new URLSearchParams(window.location.search).get("query") || "";
	let day   = new URLSearchParams(window.location.search).get("day") || "";
	
	if (query) {
		document.querySelector("#query").value = query;
		document.querySelector("#day").value   = day;
		loadData(query, day);
		updateDateRange(day);
	}
	
	document.querySelector("#search_button").addEventListener("click", function() {
		validateQuery();
	});

	document.querySelector("#dayUpdateButton").addEventListener("click", function() {
		let newDay = document.querySelector("#day").value;
		updateDateRange(newDay);
		loadData(document.querySelector("#query").value, newDay);
	});
});

/* 비동기 데이터 로딩 */
function loadData(query, day) {
	
	console.log("[query] " + query + " [day] " + day);
	
	fetch(`data.jsp?query=${query}&day=${day}`)
		.then(response => response.json())
		.then(data => {
			stockData = data.stockNames;
			load_stackData(data.stackData);
			updateHotNews(data.hotNewsData);
			load_pieData(data.pieData);
			updateBoardData(data.boardData);
		})
		.catch(error => console.error("DATA LOADING ERROR : ", error));
}

function updateHotNews(hotNews) {
	let table = document.querySelector("#hotNewsTable");
	table.innerHTML = "";
	
	hotNews.forEach((news, i) => {
		
		let title_row   = document.createElement("tr");
		let comment_row = document.createElement("tr");
		
		title_row.innerHTML = `
			<td>${i + 1}</td>
			<td>${news.date}</td>
			<td><a href="${news.link}" target="_blank">${news.title}</a></td>
		`;
		
		comment_row.innerHTML = `
			<td></td>
			<td></td>
			<td>${news.comment} [추천수 ${news.up}]</td>
		`;
		
		/*row.innerHTML = `
				<td>${i + 1}</td>
				<td>${news.date}</td>
				<td><a href="${news.link}" target="_blank">${news.title}</a></td>
			</tr>
			<tr>
				<td></td>
				<td></td>
				<td>${news.comment} [추천수 ${news.up}]</td>
		`;*/
		
		table.appendChild(title_row);
		table.appendChild(comment_row);
	});
}

function updateBoardData(boardData) {
	let table = document.querySelector("#boardTable");
	table.innerHTML = "";
	
	boardData.forEach((post, i) => {
		
		let row = document.createElement("tr");
		
		row.innerHTML = `
			<td>${i + 1}</td>
			<td>${post.date}</td>
			<td><a href="${post.link}" target="_blank">${post.title}</a></td>
			<td>${post.view}</td>
			<td>${post.up}</td>
			<td>${post.down}</td>
		`;
		table.appendChild(row);
	});
}

function updateCharts(stackData, pieData) {
	load_stackData(stackData);
	load_pieData(pieData);
}

/* 차트 헤더 날짜 표시 & 업데이트*/
function formatDate(date) {

	let year = date.getFullYear();
	let month = ("0" + (date.getMonth() + 1)).slice(-2);
	let day = ("0" + (date.getDate())).slice(-2);

	let formattedDate = year + "." + month + "." + day

	return formattedDate;
}

function updateDateRange(dayVal) {

	dayVal = parseInt(dayVal);

	let today     = new Date();
	let startDate = new Date();

	startDate.setDate(today.getDate() - (dayVal - 1));

	let range = formatDate(startDate) + "~" + formatDate(today);
	document.querySelector(".dateRange").innerText = range;
}

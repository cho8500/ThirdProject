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
		validateQuery(stockData);
	});

	document.querySelector("#dayUpdateButton").addEventListener("click", function() {
		let newDay = document.querySelector("#day").value;

		updateDateRange(newDay);
		loadData(document.querySelector("#query").value, newDay);
	});

	document.querySelector("#day").addEventListener("keydown", function(event) {
		if (event.key === "Enter") {
			let newDay = document.querySelector("#day").value;

			updateDateRange(newDay);
			loadData(document.querySelector("#query").value, newDay);
		}
	});

	document.querySelector("#hamburgerButton").addEventListener("click", function() {
		let stockDropdown = document.querySelector("#stockDropdown");

		stockDropdown.style.display = stockDropdown.style.display === "block" ? "none" : "block";
	});

	document.addEventListener("click", function(event) {
		let hamburgerButton = document.querySelector("#hamburgerButton");
		let stockDropdown   = document.querySelector("#stockDropdown");

		if (!hamburgerButton.contains(event.target) && !stockDropdown.contains(event.target)) {
			stockDropdown.style.display = "none";
		}
	});
});

/* 차트 헤더 날짜 표시 & 업데이트 */
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

	let range = formatDate(startDate) + " ~ " + formatDate(today);
	document.querySelector("#day").value = dayVal;
	document.querySelector("#dateRange").innerText = range;
	document.querySelectorAll(".descDay").forEach(item => {
		item.innerText = dayVal;
	});
}

/* 햄버거 메뉴 종목 업데이트 */
function setupHamburgerMenu(stockData) {

	let stockDropdown = document.querySelector("#stockDropdown");

	stockDropdown.innerHTML = "";

	stockData.forEach(stock => {

		let stockItem = document.createElement("a");

		stockItem.textContent = stock.name;
		stockItem.href = "#";
		stockItem.onclick = function() {
			loadData(stock.name, 30);
			updateDateRange(30);
			stockDropdown.style.display = "none";
		};
		stockDropdown.appendChild(stockItem);
	});
}

/* 비동기 데이터 로딩 */
function loadData(query, day) {

	let code          = "";
	let companyName   = "";

	fetch(`data.jsp?query=${query}&day=${day}`)
		.then(response => response.json())
		.then(data => {

			if(stockData.length == 0) {
				data.stockNames.forEach( item => stockData.push(item) );
			};
			load_stackData(data.stackData);
			load_tradingVol(data.tradingVol);
			updateHotNews(data.hotNewsData);
			load_pieData(data.pieData);
			updateBoardData(data.boardData);

			setupHamburgerMenu(stockData);
			stockData.forEach(stock => {

				if (stock.name == query) {
					code = stock.code;
					companyName = query;
					return;
				}
			});
			document.querySelector("#query").value = query;
			document.querySelector("#companyName").innerHTML = `
				${query} <span style="color: #AAA;">(${code})</span>
			`;
			document.querySelector("#query").value = query;
		})
		.catch(error => console.error("DATA LOADING ERROR : ", error));

	console.log("[query] " + query + " [day] " + day);
}

/* 핫뉴스 테이블 업데이트 */
function updateHotNews(hotNews) {
	let table = document.querySelector("#hotNewsTable tbody");
	table.innerHTML = "";

	hotNews.forEach((news, i) => {

		let title_row   = document.createElement("tr");
		let comment_row = document.createElement("tr");

		title_row.innerHTML = `
			<td style="text-align: center;">${i + 1}</td>
			<td style="text-align: center;">${news.date}</td>
			<td style="padding-left: 10px;"><a href="${news.link}" target="_blank">${news.title}</a></td>
			<td></td>
		`;

		comment_row.innerHTML = `
			<td></td>
			<td></td>
			<td style="padding-left: 10px;"> <span style="color: #999;">COMMENT</span> : ${news.comment}</td>
			<td style="padding-left: 10px; text-align: right;">[추천수 <span style="color: #f00;">${news.up}</span>]
		`;
		table.appendChild(title_row);
		table.appendChild(comment_row);
	});
}

/* 종토방 게시글 테이블 업데이트 */
function updateBoardData(boardData) {
	let table = document.querySelector("#boardTable tbody");
	table.innerHTML = "";

	boardData.forEach((post, i) => {

		let row = document.createElement("tr");

		row.innerHTML = `
			<td style="text-align: center;">${i + 1}</td>
			<td style="text-align: center;">${post.date}</td>
			<td style="padding-left: 30px;"><a href="${post.link}" target="_blank">${post.title}</a></td>
			<td style="text-align: center;">${post.view}</td>
			<td style="text-align: center; color: red;">${post.up}</td>
			<td style="text-align: center; color: blue;">${post.down}</td>
		`;
		table.appendChild(row);
	});
}

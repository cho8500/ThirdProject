/**
 *  검색창 스크립트
 */

document.addEventListener("DOMContentLoaded", function() {
	
	let searchInput = document.querySelector("#query");

	searchInput.addEventListener("keydown", function(event) {
		if (event.key === "Enter") {
			event.preventDefault();
			validateQuery();
		}
	});
});

/* 자동완성 */
function autoComplete() {

	let query = document.querySelector("#query").value.toUpperCase().trim();
	let list  = document.querySelector("#autocomplete_list");

	list.innerHTML = "";
	list.style.display = "none";

	if (query.length === 0) { return; }

	let filteredStocks = stockData.filter(stock =>
		stock.name.includes(query) || stock.code.includes(query)
	);

	if (filteredStocks.length > 0) {
		list.style.display = "block";

		filteredStocks.forEach(stock => {
			let item = document.createElement("div");
			item.innerHTML = `${stock.name} (${stock.code})`;

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

/* 검색어 유사도 검사 */
function findClosestMatch(inputValue) {

	inputValue = inputValue.toUpperCase().trim(); // 앞뒤 공백 제거

	let bestMatch = "";
	let candidates = [];
	let bestMatchDistance = Infinity;

	stockData.forEach(stock => {
		if (stock.name.includes(inputValue)) {
			candidates.push(stock.name);
		}
	});

	if (candidates.length > 0) {
		return candidates.reduce((a, b) => a.length <= b.length ? a : b);
	}

	stockData.forEach(stock => {

		let distance = levenshteinDistance(inputValue, stock.name);

		if (distance < bestMatchDistance) {
			bestMatchDistance = distance;
			bestMatch = stock.name;
		}
	});
	return bestMatch;
}

// 레벤슈타인 거리 알고리즘 (문자열 유사도 계산)
function levenshteinDistance(a, b) {
	const matrix = Array.from({ length: a.length + 1 }, () =>
		Array(b.length + 1).fill(0)
	);

	for (let i = 0; i <= a.length; i++) matrix[i][0] = i;
	for (let j = 0; j <= b.length; j++) matrix[0][j] = j;

	for (let i = 1; i <= a.length; i++) {
		for (let j = 1; j <= b.length; j++) {
			const cost = a[i - 1] === b[j - 1] ? 0 : 1;
			matrix[i][j] = Math.min(
				matrix[i - 1][j] + 1,
				matrix[i][j - 1] + 1,
				matrix[i - 1][j - 1] + cost
			);
		}
	}
	return matrix[a.length][b.length];
}

function validateQuery() {

	let queryInput = document.querySelector("#query").value.trim();
	let found = stockData.some(stock => stock.name === queryInput);

	if (!found) {
		let closestMatch = findClosestMatch(queryInput);
		document.querySelector("#query").value = closestMatch;
		alert(`입력한 값이 존재하지 않아 "${closestMatch}"로 자동 검색됩니다.`);
	}

	window.location.href = `result.jsp?query=${document.querySelector("#query").value}&day=30`;
}
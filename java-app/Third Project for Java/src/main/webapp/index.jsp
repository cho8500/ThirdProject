<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="ezen.vo.DataVO" %>
<%@ page import="ezen.dto.DataDTO" %>
<%@ page import="ezen.dao.DbManager"%>
<%@ page import="java.util.ArrayList" %>

<%
DataDTO dto = new DataDTO();
ArrayList<DataVO> stock_list = dto.getStockNames();

System.out.println("[데이터 로드] size: " + stock_list.size());
%>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>WAGLE WAGLE</title>
		<style>
			body {
				font-family: Arial, sans-serif;
				text-align: center;
			}
			
			/* 로고 */
			#main_logo {
				margin: auto;
				width: 100%;
				height: 250px;
				padding-top: 200px;
				text-align: center;
			}
			
			#logo_img {
				width: 300px;
			}
			
			/* 검색창 */
			#search_container {
				position: relative;
				display: flex;
				justify-content: center;
				margin-top: 50px;
			}
			
			#query {
				width: 300px;
				height: 30px;
				padding: 5px 40px 5px 15px;
				border-radius: 20px;
				border: 1px solid #ccc;
				outline: none;
				font-size: 12px;
				text-align: left;
			}
			
			#search_button {
				position: absolute;
				top: 50%;
				transform: translateY(-50%);
				background: none;
				border: none;
				cursor: pointer;
			}
			
			#search_button img {
				width: 24px;
				height: 24px;
			}
			
			/* 자동완성 */
			#autocomplete_list {
				position: absolute;
				top: 50px;
				width: 320px;
				border: 1px solid #ccc;
				border-radius: 5px;
				background: white;
				display: none;
				overflow-y: auto;
				z-index: 10;
				text-align: left;
				font-size: 12px;
			}
			
			#autocomplete_list div {
				padding: 12px 20px;
				cursor: pointer;
			}
			
			#autocomplete_list div:hover {
				background: #f0f0f0;
				font-weight: bold;
			}
		</style>
	</head>
	<body>
		<!-- 로고 -->
		<div id="main_logo">
			<img id="logo_img" src="./img/logo2-removebg-preview.png">
		</div>
		
		<!-- 검색창 -->
		<div id="search_container">
			<form action="result.jsp" method="GET">
				<input type="text" id="query" name="query" placeholder="종목의 이름 또는 코드를 입력하세요"
					onkeyup="javascript:autoComplete()"
					onblur="javascript:hideAutoComplete()"
					autocomplete="off">
				<button id="search_button" type="submit">
					<img src="./img/magnifying_glass.png" alt="Search">
				</button>
			</form>
			<div id="autocomplete_list"></div>
		</div>
		
		<!-- 페이지 스크립트 -->
		<script>
			let stockData = [
				<%
				for(int i = 0; i < stock_list.size(); i++)
				{
					DataVO vo = stock_list.get(i);
					%>
					{ name : "<%= vo.getName() %>", code : "<%= vo.getCode() %>"}<%= (i < stock_list.size() - 1) ? "," : "" %>
					<%
				}
				%>
			];
			
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
						item.innerHTML = `\${stock.name} (\${stock.code})`;
						
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
		</script>
</body>
</html>
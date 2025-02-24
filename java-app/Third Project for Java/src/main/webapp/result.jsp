<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="ezen.vo.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.dao.*"%>
<%@ page import="java.util.ArrayList" %>

<%
String query = request.getParameter("query");
String day   = request.getParameter("day");

/* 검색창 자동완성 불러오기 */
DataDTO dto = new DataDTO();
ArrayList<DataVO> stockNames  = dto.getStockNames();
ArrayList<DataVO> hotNewsData = dto.getHotNews(query, day);

System.out.println("[데이터 로드] size: " + stockNames.size());
%>

<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>WAGLE WAGLE</title>
		<!-- 스타일 시트 -->
		<link rel="stylesheet" href="./css/stack.css">
		<link rel="stylesheet" href="./css/pie.css">
		
		<!-- 하이차트 스크립트 -->
		<script src="https://code.highcharts.com/highcharts.js"></script>
		<script src="https://code.highcharts.com/modules/exporting.js"></script>
		<script src="https://code.highcharts.com/modules/export-data.js"></script>
		<script src="https://code.highcharts.com/modules/accessibility.js"></script>
		
		<style>
			/* 페이지 상단 */
			#header_container {
				display: flex;
				flex-direction: column;
				align-items: center;
				position: fixed;
				top: 0;
				left: 0;
				width: 100%;
				background: #fff;
				z-index: 10;
				padding: 25px 0;
				border-bottom: 1px solid #ccc;
			}
			
			#topHeader {
				display: flex;
				justify-content: space-between;
				gap: 50px;
				align-items: center;
			}
			
			#pageHeader {
				margin-top: 30px;
				display: flex;
				gap: 20px;
				align-items: center;
			}
			
			body {
				padding-top: 120px;
			}
			
			#logo {
				height: 40px;
				margin-right: 70px
			}
			
			/* 검색창 */
			#search_container {
				position: relative;
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
				right: 10px;
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
			
			/* 페이지 헤더 */
			#pageHeader {
				text-align: center;
				margin-bottom: 10px;
			}
			
			#pageHeader span,
			#pageHeader input {
				font-size: 12px;
				vertical-align: middle;
			}
			
			#day {
				margin-left: 10px;
				width: 100px;
			}
			
			#dateRange {
				margin-left: 10px;
				font-size: 14px;
				color: #555;
			}
			
			/* 파트 제목 */
			.part_title {
				font-size: 20px;
				font-weight: bold;
				position: absolute;
				left: 25%;
				top: -40px;
			}
			
			 .part_container {
			 	position: relative;
			 	margin-top: 60px;
			 	padding-top: 30px;
			 }
			
			/* 핫뉴스 테이블 컨테이너 */
			#hotNew_container {
				display: flex;
				flex-direction: column;
				align-items: center;
				justify-content: center;
				text-align: center;
			}
			
			/* 핫뉴스 테이블 */
			#hotNewsTable {
				border-collapse: collapse;
				width: 80%;
				max-width: 900px;
				margin: 0 auto;
				text-align: center;
				border: 1px solid #ccc;
			}
			
			#hotNewsTable th, #hotNewsTable td {
				padding: 10px;
				border: 1px solid #ddd;
			}
			
			#hotNewsTable tr:nth-child(even) {
				background-color: #f9f9f9;
			}
			
			#hotNewsTable tr:hover {
				background-color: #f1f1f1;
			}
			</style>
	</head>
	<body>
		<div id="header_container">
			<div id="topHeader">
				<!-- 로고 -->
				<a href="./index.jsp"><img id="logo" src="./img/logo4.PNG"></a>
				
				<!-- 검색창 -->
				<div id="search_container">
					<form action="result.jsp" method="GET" onsubmit="return validateQuery()">
						<input type="hidden" name="day" value="90">
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
			</div>
			
			<!-- 이름 & 날짜 표시 -->
			<div id="pageHeader">
				<span id="companyName"><%= query %></span>
				<input type="number" id="day" value="<%= day %>" min="7">
				<button id="dayUpdateButton">적용</button>
				<span class="dateRange"></span>
			</div>
		</div>
			
		<!-- 스택차트 파트 -->
		<div id="stackChart_container" class="part_container">
			<h3 class="part_title">뉴스 분석 결과</h3>
			<figure class="stackcharts-figure">
				<div id="stackChart"></div>
			</figure>
		</div>
		
		<!-- 핫뉴스 파트 -->
		<div id="hotNew_container" class="part_container">
			<h3 class="part_title">핫 뉴스</h3>
			<span class="dateRange"></span>
			<table id="hotNewsTable">
				<tr>
					<td colspan="3">
						[ <%= query %> ] <%= day %>일 내에 가장 많은 댓글이 달린 뉴스입니다. -클릭시 해당 뉴스로 이동
					</td>
				</tr>
				<%
				for(int i = 0; i < hotNewsData.size(); i++)
				{
					DataVO vo = hotNewsData.get(i);
					%>
					<tr>
						<th><%= i + 1 %></th>
						<td><%= vo.getDate() %></td>
						<td><a href="<%= vo.getLink() %>"><%= vo.getTitle() %></a></td>
					</tr>
					<tr>
						<td></td>
						<td></td>
						<td><%= vo.getComment() %> [추천수]<%= vo.getUp() %></td>
					</tr>
					<%
				}
				 %>
			</table>
		</div>
		
		
		<!-- 파이차트 파트 -->
		<div id="pieChart_container" class="part_container">
			<h3 class="part_title">종토방 온도계</h3>
			<figure class="piecharts-figure">
				<div id="pieChart"></div>
			</figure>
		</div>
		
		<!-- 스크립트 -->
		<script src="./js/index.js"></script>
		<script src="./js/stack.js"></script>
		<script src="./js/pie.js"></script>
		<script>
		/* 검색창 자동완성 불러오기 */
		let stockData = [
			<%
			for(int i = 0; i < stockNames.size(); i++)
			{
				DataVO vo = stockNames.get(i);
				%>
				{ name : "<%= vo.getName() %>", code : "<%= vo.getCode() %>"}<%= (i < stockNames.size() - 1) ? "," : "" %>
				<%
			}
			%>
		];
		
		/* 차트 업데이트 */
		function updateChart() {
			let query = document.querySelector("#query").value;
			let day   = document.querySelector("#day").value;
			
			updateDateRange(day);
			load_stackData(query, day);
		}
		
		/* 차트 헤더 날짜 표시 & 업데이트*/
		function formatDate(date) {
			
			let year  = date.getFullYear();
			let month = ("0" + (date.getMonth() + 1)).slice(-2);
			let day   = ("0" + (date.getDate())).slice(-2);
			
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
		
		/* window onload */
		document.addEventListener("DOMContentLoaded", function() {
			
			let query = "<%= query %>";
			let day   = "<%= day %>";
			
			updateDateRange(day);
			load_stackData(query, day);
			
			document.querySelector("#day").addEventListener("change", function() {
				
				let dayInput = this.value;
				updateDateRange(dayInput);
				load_stackData(query, dayInput);
			});
			
			document.querySelector("#dayUpdateButton").addEventListener("click", function() {
				updateChart();
			})
		});
		</script>
	</body>
</html>
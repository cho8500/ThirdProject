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
ArrayList<DataVO> stockNames = dto.getStockNames();

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
				align-item: center;
				justify-content: center;
				position: fixed;
				top: 0;
				left: 0;
				width: 100%;
				background: #fff;
				z-index: 10;
				padding: 30px 0;
				border-bottom: 1px solid #ccc;
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
			</style>
	</head>
	<body>
		<div id="header_container">
			<img id="logo" src="./img/logo4.PNG">
			
			<!-- 검색창 -->
			<div id="search_container">
				<form action="result.jsp" method="GET">
					<input type="text" id="query" name="query" placeholder="종목의 이름 또는 코드를 입력하세요"
						onkeyup="javascript:autoComplete()"
						onblur="javascript:hideAutoComplete()"
						autocomplete="off">
						
					<button id="search_button" type="submit">
						<img src="./img/magnifying_glass.png" alt="Search"></button>
				</form>
				<div id="autocomplete_list"></div>
			</div>
		</div>
		<!-- 스택그래프 : 뉴스 댓글 -->
		<figure class="highcharts-figure">
			<div id="stackchart"></div>
		</figure>
		
		<!-- 파이그래프 : 종목토론방 -->
		<figure class="highcharts-figure">
			<div id="piechart"></div>
		</figure>
		
		<!-- 스크립트 -->
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
		</script>
		<script src="./js/index.js"></script>
	</body>
</html>
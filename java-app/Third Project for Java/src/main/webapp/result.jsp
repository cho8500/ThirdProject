<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="ezen.vo.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.dao.*"%>
<%@ page import="java.util.ArrayList" %>

<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>WAGLE WAGLE</title>
		<!-- 스타일 시트 -->
		<link rel="stylesheet" href="./css/stack.css">
		<link rel="stylesheet" href="./css/pie.css">
		<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquareNeo@1.0/nanumsquareneo.css" rel="stylesheet">
		
		<!-- 하이차트 라이브러리 -->
		<script src="https://code.highcharts.com/highcharts.js"></script>
		<script src="https://code.highcharts.com/modules/exporting.js"></script>
		<script src="https://code.highcharts.com/modules/export-data.js"></script>
		<script src="https://code.highcharts.com/modules/accessibility.js"></script>
		
		<style>
			body, table {
				font-family: 'NanumSquareNeoLight', sans-serif;
			}
		
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
			#hotNew_container,
			#board_container {
				display: flex;
				flex-direction: column;
				align-items: center;
				justify-content: center;
				text-align: center;
			}
			
			/* 핫뉴스 테이블 */
			#hotNewsTable,
			#boardTable {
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
			
			/* 보드 데이터 테이블 */
			#boardTable {
				width: 100%;
				max-width: 500px;
				border-collapse: collapse;
				text-align: center;
				margin-top: 20px;
			}
			
			#boardTable th, #boardTable td {
				padding: 10px;
				border: 1px solid #ddd;
			}
			
			#boardTable thead {
				background-color: #f8f9fa;
				font-weight: bold;
			}
			
			#boardTable tr:nth-child(even) {
				background-color: #f9f9f9;
			}
			
			#boardTable tr:hover {
				background-color: #f1f1f1;
			cursor: pointer;
			}
			
			a {
				text-decoration: none;
				color: inherit;
				display: block;
				padding: 5px;
			}
			
			a:hover {
				color: #ff6600;
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
					<input type="text" id="query" name="query" placeholder="종목의 이름 또는 코드를 입력하세요"
						onkeyup="autoComplete()"
						onfocus="autoComplete()"
						onblur="hideAutoComplete()"
						autocomplete="off">
					<button id="search_button">
						<img src="./img/magnifying_glass.png" alt="Search">
					</button>
					<div id="autocomplete_list"></div>
				</div>
			</div>
			
			<!-- 이름 & 날짜 표시 -->
			<div id="pageHeader">
				<span id="companyName"></span>
				<input type="number" id="day" value="90" min="7">
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
			<table id="hotNewsTable" class="dataTable"></table>
		</div>
		
		
		<!-- 파이차트 파트 -->
		<div id="pieChart_container" class="part_container">
			<h3 class="part_title">종토방 온도계</h3>
			<figure class="piecharts-figure">
				<div id="pieChart"></div>
			</figure>
		</div>
		
		<!-- 종토방 댓글 파트 -->
		<div id="board_container" class="part_container">
			<h3 class="part_title">종토방 인기 게시글</h3>
			<table id="boardTable" class="dataTable"></table>
		</div>
		
		<!-- 스크립트 -->
		<script src="./js/stack.js"></script>
		<script src="./js/pie.js"></script>
		<script src="./js/searchbar.js"></script>
		<script src="./js/result.js"></script>
	</body>
</html>
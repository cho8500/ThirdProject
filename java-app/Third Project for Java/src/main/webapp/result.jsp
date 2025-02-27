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
		<!-- 스타일 시트 -------------------------------------------------------------------->
		<link rel="stylesheet" href="./css/stack.css">
		<link rel="stylesheet" href="./css/pie.css">
		<link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
		<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100..900&display=swap" rel="stylesheet">
		
		<!-- 하이차트 라이브러리 --------------------------------------------------------------->
		<script src="https://code.highcharts.com/highcharts.js"></script>
		<script src="https://code.highcharts.com/modules/exporting.js"></script>
		<script src="https://code.highcharts.com/modules/export-data.js"></script>
		<script src="https://code.highcharts.com/modules/accessibility.js"></script>
		
		<style>
			body, table, input, button {
				font-family: "Noto Sans KR", serif;
			}
			
			body {
				display: flex;
				flex-direction: column;
				align-items: center;
				height: 100vh;
				margin: 0;
				padding-top: 180px;
			}
			
			a {
				text-decoration: none;
				color: inherit;
			}
			
			a:hover {
				color: #ff6666;
			}
			
			.container {
				display: flex;
				flex-direction: column;
				width: 100%;
				height: clac(100vh - 180px);
			}
			
			#logo {
				height: 40px;
				margin-right: 70px
			}
			
			/* 상단 고정탭 */
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
			
			/* 로고, 검색창 */
			#topHeader {
				display: flex;
				justify-content: space-between;
				align-items: center;
			}
			
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
			
			/* 이름, 날짜 표시 */
			#pageHeader {
				margin-top: 30px;
				display: flex;
				align-items: end;
			}
			
			#companyName {
				font-size: 25px;
				font-weight: 800;
			}
			
			#dateRange {
				margin-left: 15px;
				font-size: 15px;
				color: #555;
			}
			
			#day {
				text-align: center;
				font-size: 15px;
				margin-left: 40px;
				margin-right: 10px;
				width: 70px;
				height: 30px;
				outline: none;
				border: none;
				border-bottom: 1.5px solid #ccc;
				transition: border-bottom 0.3s;
			}
			
			#day::-webkit-outer-spin-button,
			#day::-webkit-inner-spin-button {
				-webkit-appearance: none;
				margin: 0;
			}
			
			#day:focus {
				outline: none;
				border-bottom: 1.5px solid #aaa;
			}
			
			#dayUpdateButton {
				text-align: center;
				border-radius: 5px;
				width: 70px;
				outline: none;
				border: none;
				height: 30px;
				cursor: pointer;
				transition: all 0.2s
			}
			
			#dayUpdateButton:hover {
				background: #555;
				color: #fff;
			}
			
			/* 햄버거 메뉴 */
			#hamburgerButton {
				position: fixed;
				top: 110px;
				right: 40px;
				background: none;
				border: none;
				cursor: pointer;
			}
			
			#hamburgerButton img {
				width: 25px;
				height: 25px;
			}
			
			.dropdown-content {
				display: none;
				position: fixed;
				top: 110px;
				right: 40px;
				background-color: white;
				box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
				border-radius: 5px;
				width: 300px;
				max-height: 500px;
				overflow-y: auto;
			}
			
			.dropdown-content a {
				display: block;
				padding: 12px;
				text-decoration: none;
				color: black;
				font-size: 16px;
				border-bottom: 1px solid #ddd;
				cursor: pointer;
			}
			
			.dropdown-content a:hover {
				background-color: #f1f1f1;
			}
			
			/* 탭 하단부 */
			 .part_container {
			 	flex: 1;
			 	display: flex;
			 	flex-direction: column;
			 	align-items: center;
			 	justify-content: center;
			 	width: 100%;
			 	margin: 40px 0;
			 	position: relative;
			 }
			 
			.part_title {
				position: relative;
				left: 20%;
				text-align: left;
				max-width: 80%;
				align-self: flex-start;
				margin-bottom: 15px;
				font-size: 30px;
				font-weight: 700;
				color: #333;
			}
			
			.desc {
				position: relative;
				left: 20%;
				text-align: left;
				max-width: 80%;
				align-self: flex-start;
				margin-bottom: 30px;
				font-size: 16px;
				font-weight: 400;
				color: #555;
			}
			
			#stackChart_container {
				margin-bottom: 0;
			}
			
			.dataTable {
				left: 40%;
				width: 60%;
				border-collapse: collapse;
			}
			
			.dataTable tr {
				height: 40px;
			}
			
			.dataTable td {
				white-space: nowrap;
				overflow: hidden;
				text-overflow: ellipsis;
			}
			
			#hotNewsTable th,
			#hotNewsTable tr:nth-child(even) td {
				border-bottom: 1px solid #CCC;
			}
			
			#boardTable th,
			#boardTable td {
				border-bottom: 1px solid #CCC;
			}
			
			#board_container {
				margin-bottom: 200px;
			}
			</style>
	</head>
	<body>
		<!-- 상단 고정탭 -------------------------------------------------------------------->
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
				<span id="dateRange"></span>
				<input type="number" id="day" value="90" min="7" placeholder="day">
				<button id="dayUpdateButton">일 보기</button>
			</div>
			
			<!-- 햄버거 메뉴 -->
			<button id="hamburgerButton"><img src="./img/bars.png"></button>
			<div id="stockDropdown" class="dropdown-content"></div>
		</div>
		
		<!-- 탭 하단부 -------------------------------------------------------------------->
		<div class=container>
			<!-- 스택차트 파트 -->
			<div id="stackChart_container" class="part_container">
				<span class="part_title">뉴스 분석 결과</span>
				<span class="desc">
					<span class="descDay"></span>일 내 종목과 관련된 뉴스의 댓글을 모아서 분석한 결과입니다. 하단의 거래량 차트와 함께 표시됩니다.
				</span>
				<figure class="stackcharts-figure">
					<div id="stackChart"></div>
				</figure>
			</div>
			
			<!-- 거래량차트 파트 -->
			<div id="columnChart_container" class="part_container">
				<figure class="columncharts-figure">
					<div id="tradingChart"></div>
				</figure>
			</div>
			
			<!-- 핫뉴스 파트 -->
			<div id="hotNew_container" class="part_container">
				<span class="part_title">핫 뉴스</span>
				<span class="desc">
					<span class="descDay"></span>일 내 핫한 기사와 가장 많은 추천을 받은 댓글입니다. 제목 클릭시 해당 페이지로 이동합니다.
				</span>
				<table id="hotNewsTable" class="dataTable">
					<thead>
						<tr>
							<th style="width: 70px;">순위</th>
							<th style="width: 150px;">날짜</th>
							<th>제목</th>
							<th style="width: 60px;"><th>
						</tr>
					</thead>
					<tbody></tbody>
				</table>
			</div>
			
			<!-- 파이차트 파트 -->
			<div id="pieChart_container" class="part_container">
				<span class="part_title">종토방 온도계</span>
				<span class="desc">
					<span class="descDay"></span>일 내 네이버 증권의 종목토론방의 게시물들을 분석한 결과입니다.
				</span>
				<figure class="piecharts-figure">
					<div id="pieChart"></div>
				</figure>
			</div>
			
			<!-- 종토방 댓글 파트 -->
			<div id="board_container" class="part_container">
				<span class="part_title">종토방 인기 게시글</span>
				<span class="desc">
					<span class="descDay"></span>일 내 종목토론방 게시글 중 가장 많은 추천을 받은 게시글입니다. 제목 클릭시 해당 페이지로 이동합니다.
				</span>
				<table id="boardTable" class="dataTable">
					<thead>
						<tr>
							<th style="width: 70px;">순위</th>
							<th style="width: 150px;">날짜</th>
							<th>제목</th>
							<th style="width: 120px;">조회수</th>
							<th style="width: 120px;">추천</th>
							<th style="width: 120px;">비추천</th>
						</tr>
					</thead>
					<tbody></tbody>
				</table>
			</div>
		</div>
		
		<!-- 스크립트 -------------------------------------------------------------------->
		<script src="./js/stack.js"></script>
		<script src="./js/column.js"></script>
		<script src="./js/pie.js"></script>
		<script src="./js/searchbar.js"></script>
		<script src="./js/result.js"></script>
	</body>
</html>
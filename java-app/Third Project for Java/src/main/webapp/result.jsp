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
				display: block;
				padding: 5px;
			}
			
			a:hover {
				color: #ff6600;
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
			
			/* 탭 하단부 */
			 .part_container {
			 	flex: 1;
			 	display: flex;
			 	flex-direction: column;
			 	align-items: center;
			 	justify-content: center;
			 	width: 100%;
			 	padding: 40px 0;
			 	position: relative;
			 }
			 
			.part_title,
			.desc {
				position: relative;
				left: 25%;
				transform: translateX(-25%);
				text-align: left;
				max-width: 80%;
				align-self: flex-start;
				margin-bottom: 10px;
			}
			
			.part_title {
				font-size: 14px;
				color: #666;
			}
			
			.stackcharts-figure,
			.piecharts-figure,
			#hotNewsTable,
			#boardTable {
				width: 80%;
				max-width: 1500px;
			}
			
			/* 
			#hotNew_container,
			#board_container {
				display: flex;
				flex-direction: column;
				align-items: center;
				justify-content: center;
				text-align: center;
			}
			
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
			 */
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
		</div>
		
		<!-- 탭 하단부 -------------------------------------------------------------------->
		<div class=container>
			<!-- 스택차트 파트 -->
			<div id="stackChart_container" class="part_container">
				<h2 class="part_title">뉴스 분석 결과</h2>
				<span class="desc">
					기간내 종목과 관계된 뉴스의 댓글을 모아서 분석한 결과입니다.
				</span>
				<figure class="stackcharts-figure">
					<div id="stackChart"></div>
				</figure>
			</div>
			
			<!-- 핫뉴스 파트 -->
			<div id="hotNew_container" class="part_container">
				<h2 class="part_title">핫 뉴스</h2>
				<span class="desc">
					가장 많은 댓글이 달긴 기사들과 그 안에서 가장 많은 추천을 받은 댓글입니다.<br>
					기사 제목 클릭시 해당 페이지로 이동합니다.
				</span>
				<table id="hotNewsTable" class="dataTable"></table>
			</div>
			
			
			<!-- 파이차트 파트 -->
			<div id="pieChart_container" class="part_container">
				<h2 class="part_title">종토방 온도계</h2>
				<span class="desc">
					기간내 네이버 증권의 종목토론방의 게시물들을 분석한 결과입니다.
				</span>
				<figure class="piecharts-figure">
					<div id="pieChart"></div>
				</figure>
			</div>
			
			<!-- 종토방 댓글 파트 -->
			<div id="board_container" class="part_container">
				<h2 class="part_title">종토방 인기 게시글</h2>
				<span class="desc">
					종목토론방 게시글 중 가장 많은 추천을 받은 게시글입니다.
					게시글 제목 클릭시 해당 페이지로 이동합니다.
				</span>
				<table id="boardTable" class="dataTable"></table>
			</div>
		</div>
		
		<!-- 스크립트 -------------------------------------------------------------------->
		<script src="./js/stack.js"></script>
		<script src="./js/pie.js"></script>
		<script src="./js/searchbar.js"></script>
		<script src="./js/result.js"></script>
	</body>
</html>
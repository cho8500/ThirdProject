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
		<link rel="stylesheet" href="./css/result.css">

		<!-- 글꼴 ------------------------------------------------------------------------->
		<link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
		<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100..900&display=swap" rel="stylesheet">

		<!-- 하이차트 라이브러리 --------------------------------------------------------------->
		<script src="https://code.highcharts.com/highcharts.js"></script>
		<script src="https://code.highcharts.com/modules/exporting.js"></script>
		<script src="https://code.highcharts.com/modules/export-data.js"></script>
		<script src="https://code.highcharts.com/modules/accessibility.js"></script>
		<script>
			const stockData = [];
		</script>
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
						onkeyup="autoComplete(stockData)"
						onfocus="autoComplete(stockData)"
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
		<script src="./js/searchbar.js"></script>
		<script src="./js/stack.js"></script>
		<script src="./js/column.js"></script>
		<script src="./js/pie.js"></script>
		<script src="./js/result.js"></script>
	</body>
</html>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="ezen.vo.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.dao.*"%>
<%@ page import="java.util.ArrayList" %>

<%
String query = request.getParameter("query");
String day   = request.getParameter("day");
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
	</head>
	<body>
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
	</body>
</html>
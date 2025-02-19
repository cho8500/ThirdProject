<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="ezen.vo.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.dao.*"%>
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
		<link rel="stylesheet" href="./css/index.css">
	</head>
	<body>
		<!-- 로고 -->
		<div id="main_logo">
			<img id="logo_img" src="./img/logo3.PNG">
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
		</script>
		<script src="./js/index.js"></script>
</body>
</html>
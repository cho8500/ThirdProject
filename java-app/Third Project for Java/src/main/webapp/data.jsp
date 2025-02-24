<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="ezen.vo.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.dao.*"%>
<%@ page import="java.util.ArrayList" %>
<%@ page import="com.google.gson.Gson" %>
<%@ page import="com.google.gson.JsonObject"%>

<%
String query = request.getParameter("query");
String day   = request.getParameter("day");

if(query == null || day == null)
{
	response.setContentType("application/json");
	response.setCharacterEncoding("UTF-8");
	out.print("{\"error\": \"Invalid request\"}");
	out.flush();
	return;
}

DataDTO dto = new DataDTO();

/* 데이터 호출 */
ArrayList<DataVO> stockNames  = dto.getStockNames();
ArrayList<DataVO> stackData   = dto.getStackData(query, day);
ArrayList<DataVO> pieData     = dto.getPieData(query, day);
ArrayList<DataVO> hotNewsData = dto.getHotNews(query, day);
ArrayList<DataVO> boardData   = dto.getBoardData(query, day);

JsonObject jsonResponse = new JsonObject();
jsonResponse.add("stockNames",  new Gson().toJsonTree(stockNames));
jsonResponse.add("stackData",   new Gson().toJsonTree(stackData));
jsonResponse.add("pieData",     new Gson().toJsonTree(pieData));
jsonResponse.add("hotNewsData", new Gson().toJsonTree(hotNewsData));
jsonResponse.add("boardData",   new Gson().toJsonTree(boardData));

response.setContentType("application/json");
response.setCharacterEncoding("UTF-8");

out.print(jsonResponse.toString());
out.flush();
%>
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

boolean pageFlag = false;

if (query == null) pageFlag = true;

DataDTO dto = new DataDTO();

ArrayList<DataVO> stockNames  = null;
ArrayList<DataVO> stackData   = null;
ArrayList<DataVO> tradingVol  = null;
ArrayList<DataVO> hotNewsData = null;
ArrayList<DataVO> pieData     = null;
ArrayList<DataVO> boardData   = null;

/* 데이터 호출 */
if(pageFlag)
{
	stockNames  = dto.getStockNames();
} else {
	stockNames  = dto.getStockNames();
	stackData   = dto.getStackData(query, day);
	tradingVol  = dto.getTradingVol(query, day);
	hotNewsData = dto.getHotNews(query, day);
	pieData     = dto.getPieData(query, day);
	boardData   = dto.getBoardData(query, day);
}

JsonObject jsonResponse = new JsonObject();
jsonResponse.add("stockNames",  new Gson().toJsonTree(stockNames));
jsonResponse.add("stackData",   new Gson().toJsonTree(stackData));
jsonResponse.add("tradingVol",  new Gson().toJsonTree(tradingVol));
jsonResponse.add("hotNewsData", new Gson().toJsonTree(hotNewsData));
jsonResponse.add("pieData",     new Gson().toJsonTree(pieData));
jsonResponse.add("boardData",   new Gson().toJsonTree(boardData));

response.setContentType("application/json");
response.setCharacterEncoding("UTF-8");

out.print(jsonResponse.toString());
out.flush();
%>
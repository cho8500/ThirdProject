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

if(query == null || day == null) { response.sendRedirect("index.jsp"); }

DataDTO dto = new DataDTO();
ArrayList<DataVO> stackData = dto.getStackData(query, day);

JsonObject jsonResponse = new JsonObject();
jsonResponse.add("StackData", new Gson().toJsonTree(stackData));

response.setContentType("application/json");
response.setCharacterEncoding("UTF-8");

out.print(jsonResponse.toString());
out.flush();
%>
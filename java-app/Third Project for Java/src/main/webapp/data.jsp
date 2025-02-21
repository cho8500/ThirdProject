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

DataDTO dto = new DataDTO();

%>
package ezen.dto;

import ezen.vo.*;
import ezen.dao.*;
import java.util.ArrayList;

/**
 * 작성자 : 조강희
 * 작성일 : 2025.02.17
 * 하이차트를 그리기 위해 받아온 데이터를 처리할 DTO
 */

public class DataDTO extends DbManager
{
	/* index.jsp 검색 목록 제공 */
	public ArrayList<DataVO> getStockNames()
	{
		String sql = "SELECT * FROM stocks;";

		System.out.println("[SQL] " + sql);
		
		this.driverLoad();
		this.dbConnect();
		this.executeQuery(sql);
		
		ArrayList<DataVO> stock_list = new ArrayList<DataVO>();
		
		while(this.next())
		{
			DataVO vo = new DataVO();
			
			vo.setName(this.getString("name"));
			vo.setCode(this.getString("code"));
			
			stock_list.add(vo);
		}
		
		this.dbDisConnect();
		
		return stock_list;
	}
	
	public ArrayList<DataVO> getChartData()
	{
		String sql = "";
		sql += "SELECT ";
		sql +=		"d.date, ";
		sql +=		"s.name, ";
		sql +=		"s.code, ";
		sql +=		"s.sise, ";
		sql +=		"COALESCE(t.score, 0) AS score, ";
		sql +=		"COALESCE(t.news_count, 0) AS news_count ";
		sql += "FROM date_series d ";
		sql += "JOIN sise_data s ON d.date = s.date ";
		sql += "LEFT JOIN total_result t ON d.date = t.date AND s.name = t.name ";
		sql += "ORDER BY d.date ASC, s.name ASC;";
		
		System.out.println("[SQL] " + sql);
		
		this.driverLoad();
		this.dbConnect();
		this.executeQuery(sql);
		
		ArrayList<DataVO> data_list = new ArrayList<DataVO>();
		
		while(this.next())
		{
			DataVO vo = new DataVO();
			
			vo.setDate(this.getString("date"));
			vo.setName(this.getString("name"));
			vo.setCode(this.getString("code"));
			
			data_list.add(vo);
		}
		this.dbDisConnect();
		
		return data_list;
	}
}

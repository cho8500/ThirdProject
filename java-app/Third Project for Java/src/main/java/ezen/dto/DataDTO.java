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
		
		this.dbConnect();
		this.executeQuery(sql);
		
		ArrayList<DataVO> stockNames = new ArrayList<DataVO>();
		
		while(this.next())
		{
			DataVO vo = new DataVO();
			
			vo.setName(this.getString("name"));
			vo.setCode(this.getString("code"));
			
			stockNames.add(vo);
		}
		this.dbDisConnect();
		
		return stockNames;
	}
	
	/* stack 차트 데이터 불러오기 */
	public ArrayList<DataVO> getStackData(String query, String day)
	{
		String sql = "";
		
		sql += "SELECT dt.date, ";
		sql +=        "st.sent_type, ";
		sql +=        "IFNULL(COUNT(nc.sent_type), 0) AS count ";
		sql += "FROM date_table dt ";
		sql += "CROSS JOIN (SELECT 'positive' AS sent_type UNION ALL ";
		sql +=        "SELECT 'negative' UNION ALL ";
		sql +=        "SELECT 'neutral') st ";
		sql += "LEFT JOIN newsComments nc ";
		sql +=        "ON nc.date = dt.date ";
		sql +=        "AND nc.sent_type = st.sent_type ";
		sql +=        "AND nc.name = '" + query + "' ";
		sql += "WHERE dt.date BETWEEN CURDATE() - INTERVAL " + day + " DAY AND CURDATE() ";
		sql += "GROUP BY dt.date, st.sent_type ";
		sql += "ORDER BY dt.date ASC, ";
		sql +=        "CASE st.sent_type ";
		sql +=             "WHEN 'positive' THEN 1 ";
		sql +=             "WHEN 'neutral' THEN 2 ";
		sql +=             "WHEN 'negative' THEN 3 ";
		sql +=        "END ASC;";
		
		System.out.println("[SQL] " + sql);
		
		this.dbConnect();
		this.executeQuery(sql);
		
		ArrayList<DataVO> stackData = new ArrayList<DataVO>();
		
		while(this.next())
		{
			DataVO vo = new DataVO();
			
			vo.setDate(this.getString("date"));
			vo.setSent_type(this.getString("sent_type"));
			vo.setCount(this.getString("count"));
			
			stackData.add(vo);
		}
		this.dbDisConnect();
		
		return stackData;
	}
	
	/* 핫뉴스 데이터 불러오기 */
	public ArrayList<DataVO> getHotNews(String query, String day)
	{
		String sql = "";
		
		sql += "WITH TopArticles AS ( ";
		sql += "SELECT title, ";
		sql +=        "date, ";
		sql +=        "link, ";
		sql +=        "COUNT(*) AS comment_count ";
		sql += "FROM newsComments ";
		sql += "WHERE date > DATE_SUB(CURDATE(), INTERVAL " + day + " DAY) ";
		sql += "AND name = '" + query + "' ";
		sql += "GROUP BY title, date, link ";
		sql += "ORDER BY comment_count DESC ";
		sql += "LIMIT 5) ";
		
		sql += "SELECT ta.title, ";
		sql +=        "ta.date, ";
		sql +=        "ta.link, ";
		sql +=        "ta.comment_count, ";
		sql +=        "LEFT(c.comment, 50) AS comment, ";
		sql +=        "c.up ";
		sql += "FROM TopArticles ta ";
		sql += "JOIN newsComments c ";
		sql += "ON ta.title = c.title AND ta.date = c.date ";
		sql += "WHERE c.id = (";
		sql +=        "SELECT id ";
		sql +=        "FROM newsComments ";
		sql +=        "WHERE title = ta.title AND date = ta.date ";
		sql +=        "ORDER BY up DESC, id ASC ";
		sql +=        "LIMIT 1) ";
		sql += "ORDER BY ta.comment_count DESC, ta.date DESC;";
		
		System.out.println("[SQL] " + sql);
		
		this.dbConnect();
		this.executeQuery(sql);
		
		ArrayList<DataVO> hotNews = new ArrayList<DataVO>();
		
		while(this.next())
		{
			DataVO vo = new DataVO();
			
			vo.setTitle(this.getString("title"));
			vo.setDate(this.getString("date"));
			vo.setLink(this.getString("link"));
			vo.setCount(this.getString("comment_count"));
			vo.setComment(this.getString("comment"));
			vo.setUp(this.getString("up"));
			
			hotNews.add(vo);
		}
		this.dbDisConnect();
		
		return hotNews;
	}
	
	/* pie 차트 데이터 불러오기 */
	public ArrayList<DataVO> getPieData(String query, String day)
	{
		String sql = "";
		
		sql += "SELECT s.sent_type, COALESCE(d.count, 0) AS count FROM ";
		sql += "(SELECT 'positive' AS sent_type UNION ALL ";
		sql += "SELECT 'negative' UNION ALL ";
		sql += "SELECT 'neutral') AS s ";
		sql += "LEFT JOIN (";
		sql += "SELECT sent_type, COUNT(*) as count FROM discussion ";
		sql += "WHERE name='" + query + "' ";
		sql += "AND date BETWEEN CURDATE() - INTERVAL " + day + " DAY AND CURDATE() ";
		sql += "GROUP BY sent_type ";
		sql += ") AS d ";
		sql += "ON s.sent_type = d.sent_type;";
		
		System.out.println("[SQL] " + sql);
		
		this.dbConnect();
		this.executeQuery(sql);
		
		ArrayList<DataVO> pieData = new ArrayList<DataVO>();
		
		while(this.next())
		{
			DataVO vo = new DataVO();
			
			vo.setSent_type(this.getString("sent_type"));
			vo.setCount(this.getString("count"));
			
			pieData.add(vo);
		}
		this.dbDisConnect();
		
		return pieData;
	}
	
	public ArrayList<DataVO> getBoardData(String query, String day)
	{
		String sql = "";
		
		sql += "SELECT title, date, link, view, up, down ";
		sql += "FROM discussion ";
		sql += "WHERE name='" + query + "' ";
		sql += "AND date > DATE_SUB(CURDATE(), INTERVAL " + day + " DAY) ";
		sql += "ORDER BY up DESC ";
		sql += "LIMIT 5;";
		
		System.out.println("[SQL] " + sql);
		
		this.dbConnect();
		this.executeQuery(sql);
		
		ArrayList<DataVO> boardData = new ArrayList<DataVO>();
		
		while(this.next())
		{
			DataVO vo = new DataVO();
			
			vo.setTitle(this.getString("title"));
			vo.setDate(this.getString("date"));
			vo.setLink(this.getString("link"));
			vo.setView(this.getString("view"));
			vo.setUp(this.getString("up"));
			vo.setDown(this.getString("down"));
			
			boardData.add(vo);
		}
		this.dbDisConnect();
		
		return boardData;
	}
}

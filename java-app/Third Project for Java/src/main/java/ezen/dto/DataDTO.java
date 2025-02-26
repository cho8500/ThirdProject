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
		
		System.out.println("[SearchBar SQL] " + sql);
		
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
		sql +=        "COALESCE(COUNT(nc.sent_type), 0) AS count ";
		sql += "FROM date_table dt ";
		sql += "CROSS JOIN (";
		sql +=        "SELECT 'positive' AS sent_type UNION ALL ";
		sql +=        "SELECT 'negative' UNION ALL ";
		sql +=        "SELECT 'neutral'";
		sql += ") st ";
		sql += "LEFT JOIN newsComments nc ";
		sql +=        "ON nc.date = dt.date ";
		sql +=        "AND nc.sent_type = st.sent_type ";
		sql +=        "AND nc.name = ? ";
		sql += "WHERE dt.date BETWEEN CURDATE() - INTERVAL ? DAY AND CURDATE() ";
		sql += "GROUP BY dt.date, st.sent_type ";
		sql += "ORDER BY dt.date ASC, ";
		sql +=        "FIELD(st.sent_type, 'positive', 'neutral', 'negative');";
		
		System.out.println("[StackChart (" + query + ", " + day + ")]");
		
		this.dbConnect();
		this.executeQuery(sql, query, day);
		
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
		sql += "WHERE name = ? ";
		sql += "AND date > DATE_SUB(CURDATE(), INTERVAL ? DAY) ";
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
		sql += "LEFT JOIN newsComments c2 ";
		sql += "ON c.title = c2.title AND c.date = c2.date AND c.up < c2.up ";
		sql += "WHERE c2.id IS NULL ";
		sql += "ORDER BY ta.comment_count DESC, ta.date DESC;";
		
		System.out.println("[HotNews    (" + query + ", " + day + ")]");
		
		this.dbConnect();
		this.executeQuery(sql, query, day);
		
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
		
		sql += "SELECT ";
		sql +=     "s.sent_type, ";
		sql +=     "COALESCE(d.count, 0) AS count ";
		sql += "FROM (";
		sql +=     "SELECT 'positive' AS sent_type UNION ALL ";
		sql +=     "SELECT 'negative' UNION ALL ";
		sql +=     "SELECT 'neutral'";
		sql += ") AS s ";
		sql += "LEFT JOIN (";
		sql +=     "SELECT sent_type, ";
		sql +=     "COUNT(*) as count ";
		sql +=     "FROM discussion ";
		sql +=     "WHERE name=? ";
		sql +=     "AND date BETWEEN CURDATE() - INTERVAL ? DAY AND CURDATE() ";
		sql +=     "GROUP BY sent_type ";
		sql += ") AS d ";
		sql += "ON s.sent_type = d.sent_type;";
		
		System.out.println("[PieChart   (" + query + ", " + day + ")]");
		
		this.dbConnect();
		this.executeQuery(sql, query, day);
		
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
		
		sql += "SELECT ";
		sql +=     "title, ";
		sql +=     "date, ";
		sql +=     "link, ";
		sql +=     "view, ";
		sql +=     "up, ";
		sql +=     "down ";
		sql += "FROM discussion ";
		sql += "WHERE name=? ";
		sql += "AND date > DATE_SUB(CURDATE(), INTERVAL ? DAY) ";
		sql += "ORDER BY up DESC ";
		sql += "LIMIT 5;";
		
		System.out.println("[BoardData  (" + query + ", " + day + ")]");
		
		this.dbConnect();
		this.executeQuery(sql, query, day);
		
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

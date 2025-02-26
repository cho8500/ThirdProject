package ezen.dao;

import java.sql.*;
import org.apache.commons.dbcp2.BasicDataSource;

// 데이터에 접근할 수 있는 메소드를 담은 DAO 클래스
public class DbManager
{
	Connection conn         = null;
	PreparedStatement pstmt = null;
	ResultSet  rs           = null;
	
	private static BasicDataSource dataSource;
	
	static {
		String className = "com.mysql.cj.jdbc.Driver";
		
		String url       = "jdbc:mysql://192.168.0.184:3306/third_project";
		String id        = "cho";
		String pw        = "ezen";
		
//		String url       = "jdbc:mysql://localhost:3306/third_project";
//		String id        = "root";
//		String pw        = "chogh";
		
		dataSource = new BasicDataSource();
		
		dataSource.setDriverClassName(className);
		dataSource.setUrl(url);
		dataSource.setUsername(id);
		dataSource.setPassword(pw);
		// Pool 설정
		dataSource.setInitialSize(5);	// 초기 연결 수
		dataSource.setMaxTotal(20);		// 최대 연결 수
		dataSource.setMaxIdle(10);		// 최대 idle 연결 수
		dataSource.setMinIdle(5);		// 최소 idle 연결 수
	}

	//	Database connection
	public void dbConnect()
	{
		try {
			conn = dataSource.getConnection();
		}
		catch (SQLException e) {
			System.out.println("데이터베이스 연결 실패");
			e.printStackTrace();
		}
	}
	
//	Execute queries; create, update, delete
	public void execute(String sql, Object... params)
	{
		try
		{
			pstmt = conn.prepareStatement(sql);
			
			for(int i = 0; i < params.length; i++) {
				pstmt.setObject(i + 1, params[i]);
			}
			System.out.println("[SQL] " + pstmt.toString());
			pstmt.executeUpdate();
		}
		catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
//	Execute query; select
	public void executeQuery(String sql, Object... params)
	{
		try
		{
			pstmt = conn.prepareStatement(sql);
			
			for(int i = 0; i < params.length; i++)
			{
				pstmt.setObject(i + 1, params[i]);
			}
			System.out.println("[SQL] " + pstmt.toString());
			rs   = pstmt.executeQuery();
		}
		catch (SQLException e)
		{
			e.printStackTrace();
			dbDisConnect();
		}
	}
	
	public boolean next()
	{
		try{ return rs.next(); }
		catch (SQLException e)
		{ 
			e.printStackTrace();
			return false;
		}
	}
	
	public String getString(String column)
	{
		try { return rs.getString(column); }
		catch (SQLException e) 
		{ 
			e.printStackTrace();
			return null;
		}
	}
	
	public int getInt(String column)
	{
		try { return rs.getInt(column); }
		catch (SQLException e) 
		{ 
			e.printStackTrace();
			return -1;
		}
	}
	
//	Database disconnection
	public void dbDisConnect()
	{
		try {
			if(rs   != null) rs.close();
			if(pstmt != null) pstmt.close();
			if(conn != null) conn.close();
		} catch (SQLException e) { e.printStackTrace(); }
	}
	
//	***작은 따옴표 처리; 1개 입력시 2개로 변환
	public String _R(String value)
	{
		return value.replace("'", "''");
	}
}

package ezen.vo;

/**
 * 작성자 : 조강희
 * 작성일 : 2025.02.17
 * 하이차트를 그리기 위해 DB에서 받아온 데이터를 관리할 VO
 */

public class DataVO
{
	/* 전체 표 공통 요소 */
	private String id;			// id (daily_data table)
	private String date;		// 기사 또는 게시글 작성날짜
	private String name;		// 종목이름
	private String code;		// 종목코드
	private String title;		// 기사 또는 게시글 제목
	private String link;		// 링크
	private String up;			// 좋아요
	private String down;		// 싫어요
	private String comment;		// 댓글 또는 게시글 내용
	private String analysis;	// 감성분석 여부
	private String sent_type;	// 감성분석 타입
	private String sent_score;	// 감성분석 점수
	
	/* 표에 따라 다르게 적용 */
	private String view;		// 게시글 조회수(discussion)
	private String cmt_count;	// 댓글수(news_comments)
	private String pos_count;	// 긍정수
	private String neg_count;	// 부정수
	private String ntr_count;	// 중립수
	
	public String getId()         { return id;         }
	public String getDate()       { return date;       }
	public String getName()       { return name;       }
	public String getCode()       { return code;       }
	public String getTitle()      { return title;      }
	public String getLink()       { return link;       }
	public String getUp()         { return up;         }
	public String getDown()       { return down;       }
	public String getComment()    { return comment;    }
	public String getAnalysis()   { return analysis;   }
	public String getSent_type()  { return sent_type;  }
	public String getSent_score() { return sent_score; }
	public String getView()       { return view;       }
	public String getPos_count()  { return pos_count;  }
	public String getNeg_count()  { return neg_count;  }
	public String getNtr_count()  { return ntr_count;  }
	public String getCmt_count()  { return cmt_count;  }
	
	public void setId(String id)                 { this.id         = id;         }
	public void setDate(String date)             { this.date       = date;       }
	public void setName(String name)             { this.name       = name;       }
	public void setCode(String code)             { this.code       = code;       }
	public void setTitle(String title)           { this.title      = title;      }
	public void setLink(String link)             { this.link       = link;       }
	public void setUp(String up)                 { this.up         = up;         }
	public void setDown(String down)             { this.down       = down;       }
	public void setComment(String comment)       { this.comment    = comment;    }
	public void setAnalysis(String analysis)     { this.analysis   = analysis;   }
	public void setSent_type(String sent_type)   { this.sent_type  = sent_type;  }
	public void setSent_score(String sent_score) { this.sent_score = sent_score; }
	public void setView(String view)             { this.view       = view;       }
	public void setPos_count(String pos_count)   { this.pos_count  = pos_count;  }
	public void setNeg_count(String neg_count)   { this.neg_count  = neg_count;  }
	public void setNtr_count(String ntr_count)   { this.ntr_count  = ntr_count;  }
	public void setCmt_count(String cmt_count)   { this.cmt_count  = cmt_count;  }
	
}

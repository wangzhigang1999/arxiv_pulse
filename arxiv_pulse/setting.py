from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    database_url: str = "mysql+pymysql://root:password@localhost:3306/arxiv_pulse"
    crawl_interval_minutes: int = 60
    arxiv_categories: str = "cs.AI,cs.CV,cs.LG,cs.CL,cs.NE,cs.SE,cs.DC,cs.DS,cs.DB,cs.IR,cs.ET,cs.GL,cs.IT,cs.MA"
    arxiv_page_size: int = 100

    # Keyword monitoring settings
    keywords: str = "agent"  # Comma-separated keywords
    summary_interval_minutes: int = 10  # How often to check for new papers matching keywords

    # LLM settings
    llm_api_key: str = ""
    llm_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    llm_model: str = "qwen3-max"

    # DingTalk webhook
    dingtalk_webhook_url: str = ""

    class Config:
        env_file = ".env"


settings = Settings()

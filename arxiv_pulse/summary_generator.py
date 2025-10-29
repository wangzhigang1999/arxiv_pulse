"""AI-powered summary generator for arXiv papers."""

from loguru import logger
from openai import OpenAI

from arxiv_pulse.database import settings


class SummaryGenerator:
    """Generate Chinese summaries for arXiv papers using LLM."""

    def __init__(self):
        """Initialize the summary generator."""
        self.client = OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )
        self.model = settings.llm_model

    def generate_chinese_summary(self, title: str, summary: str) -> str | None:
        """Generate a Chinese summary of the paper.

        Args:
            title: Paper title
            summary: Original English summary

        Returns:
            Chinese summary or None if generation fails
        """
        try:
            prompt = f"""请为以下学术论文生成一个简洁的中文摘要，要求：
1. 保持学术性但通俗易懂
2. 突出论文的主要贡献和创新点
3. 控制在 200 字以内

论文标题：{title}

英文摘要：{summary}

请生成中文摘要："""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的学术论文摘要生成助手，擅长将英文学术论文转换为简洁易懂的中文摘要。",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )

            chinese_summary = response.choices[0].message.content.strip()
            logger.info(f"Generated Chinese summary for paper: {title[:50]}...")
            return chinese_summary

        except Exception as e:
            logger.error(f"Failed to generate Chinese summary for paper '{title}': {e}")
            return None


summary_generator = SummaryGenerator()

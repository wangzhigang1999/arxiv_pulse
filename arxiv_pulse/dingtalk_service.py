"""DingTalk webhook service for sending notifications."""

import json
from typing import Any

import requests
from loguru import logger

from arxiv_pulse.database import settings


class DingTalkService:
    """Send notifications to DingTalk via webhook."""

    def __init__(self):
        """Initialize the DingTalk service."""
        self.webhook_url = settings.dingtalk_webhook_url

    def send_paper_notification(self, paper_data: dict[str, Any]) -> bool:
        """Send a paper notification to DingTalk.

        Args:
            paper_data: Dictionary containing paper information

        Returns:
            True if successful, False otherwise
        """
        if not self.webhook_url:
            logger.warning("DingTalk webhook URL not configured")
            return False

        try:
            # Prepare markdown message
            title = paper_data.get("title", "Unknown Title")
            chinese_summary = paper_data.get("chinese_summary", "")
            authors = paper_data.get("authors", "")
            link = paper_data.get("link", "")
            published = paper_data.get("published", "")

            alpha_arxiv = "https://www.alphaxiv.org/abs/" + link.split("/")[-1].strip()

            # Format message
            message = {
                "msgtype": "markdown",
                "markdown": {
                    "title": "新论文推送",
                    "text": (
                        f"# 📚 新论文推送**标题：** {title}\n\n"
                        f"**作者：** {authors}\n\n"
                        f"**发布时间：** {published}\n\n"
                        f"**中文摘要：**\n{chinese_summary}\n\n"
                        f"**原文链接：** [点击查看]({link})\n\n"
                        f"**AlphaXiv：** [点击查看]({alpha_arxiv})\n\n"
                        "---\n_来自 Arxiv Pulse 自动推送_"
                    ),
                },
            }

            # Send to DingTalk
            response = requests.post(
                self.webhook_url,
                data=json.dumps(message),
                headers={"Content-Type": "application/json"},
                timeout=10,
            )

            if response.status_code == 200:
                logger.info(f"Successfully sent DingTalk notification for paper: {title[:50]}...")
                return True
            else:
                logger.error(
                    f"Failed to send DingTalk notification. Status: {response.status_code}, Response: {response.text}"
                )
                return False

        except Exception as e:
            logger.error(f"Error sending DingTalk notification: {e}")
            return False


dingtalk_service = DingTalkService()

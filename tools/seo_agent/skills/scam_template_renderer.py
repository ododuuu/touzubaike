"""
Scam Template Renderer - 模板渲染引擎
將數據填充到模板，生成基礎 Markdown 內容
"""

import os
from datetime import datetime
from typing import Dict, Optional
from .scam_data_loader import ScamDataLoader, ScamPlatform


class ScamTemplateRenderer:
    """詐騙防範頁面模板渲染器"""

    def __init__(self, template_path: Optional[str] = None):
        if template_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(current_dir, "..", "templates", "scam_guide.md")

        self.template_path = template_path
        self.data_loader = ScamDataLoader()
        self._template = None

    def load_template(self) -> str:
        """載入模板"""
        if self._template is None:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                self._template = f.read()
        return self._template

    def render(self, platform_id: str) -> Dict[str, str]:
        """
        渲染模板，返回包含基礎內容和需要 LLM 豐富化的佔位符

        Returns:
            Dict with:
            - 'markdown': 完整 markdown 內容（含佔位符）
            - 'placeholders': 需要 LLM 填充的區塊清單
            - 'platform': 平台資料
        """
        platform = self.data_loader.get_platform(platform_id)
        if platform is None:
            raise ValueError(f"Platform not found: {platform_id}")

        template = self.load_template()

        # 生成基礎數據
        pub_date = datetime.now().strftime("%Y-%m-%d")
        year = datetime.now().year

        # SEO 標題和描述
        if platform.platform_type == "scam_pattern":
            title = f"{platform.chinese_name}完整解析｜{year}最新詐騙手法與防範指南"
            h1_title = f"{platform.chinese_name}｜詐騙手法、辨識方法與自救流程【{year}最新】"
            description = f"深入解析{platform.chinese_name}的常見手法，包含真實案例分析。教你如何辨識詐騙、避免上當，以及被騙後的報案與追回流程。165反詐騙專線、警局報案完整教學。"
        else:
            title = f"{platform.chinese_name}詐騙手法大公開｜{year}最新防範指南"
            h1_title = f"{platform.chinese_name}詐騙手法大公開｜如何辨識與自救【{year}最新】"
            description = f"完整解析{platform.chinese_name}({platform.name})常見詐騙手法，包含假客服、釣魚網站等案例。教你如何辨識真假{platform.chinese_name}，以及被騙後的報案與自救流程。"

        # 生成 tags
        tags = ', '.join([f'"{kw}"' for kw in platform.keywords[:4]])
        tags += ', "詐騙防範", "加密貨幣安全"'

        # 生成詐騙手法區塊
        scam_types_section = self._render_scam_types(platform)

        # 生成警示訊號區塊
        detection_section = self._render_detection(platform)

        # 生成報案流程區塊
        report_section = self._render_report_section()

        # 生成追回流程區塊
        recovery_section = self._render_recovery_section()

        # 生成合法性區塊（基礎版，需要 LLM 豐富化）
        legitimacy_section = self._render_legitimacy(platform)

        # 填充模板
        content = template.format(
            title=title,
            description=description,
            pub_date=pub_date,
            tags=tags,
            platform_id=platform_id,
            h1_title=h1_title,
            platform_name=platform.chinese_name,
            intro_section="{intro_section}",  # LLM 填充
            legitimacy_section=legitimacy_section,
            scam_types_section=scam_types_section,
            detection_section=detection_section,
            recovery_section=recovery_section,
            report_section=report_section,
            faq_section="{faq_section}",  # LLM 填充
            conclusion_section="{conclusion_section}"  # LLM 填充
        )

        return {
            'markdown': content,
            'placeholders': ['intro_section', 'faq_section', 'conclusion_section'],
            'platform': platform,
            'metadata': {
                'title': title,
                'description': description,
                'pub_date': pub_date,
                'platform_id': platform_id,
                'platform_name': platform.chinese_name,
                'keywords': platform.keywords
            }
        }

    def _render_scam_types(self, platform: ScamPlatform) -> str:
        """渲染詐騙手法區塊"""
        lines = []

        for i, scam_type in enumerate(platform.common_scam_types, 1):
            lines.append(f"### {i}. {scam_type.name}")
            lines.append("")
            lines.append(scam_type.description)
            lines.append("")

        return "\n".join(lines)

    def _render_detection(self, platform: ScamPlatform) -> str:
        """渲染警示訊號區塊"""
        lines = []

        # 平台特定警示
        if platform.warning_signs:
            lines.append(f"### {platform.chinese_name}詐騙的警示訊號")
            lines.append("")
            for sign in platform.warning_signs:
                lines.append(f"- {sign}")
            lines.append("")

        # 通用警示
        general_signs = self.data_loader.get_general_warning_signs()
        if general_signs:
            lines.append("### 通用詐騙警示訊號")
            lines.append("")
            for sign in general_signs:
                lines.append(f"- {sign}")
            lines.append("")

        return "\n".join(lines)

    def _render_report_section(self) -> str:
        """渲染報案流程區塊"""
        channels = self.data_loader.get_report_channels("taiwan")
        lines = []

        lines.append("遇到詐騙時，請盡快透過以下管道報案：")
        lines.append("")

        for channel in channels:
            name = channel.get("name", "")
            phone = channel.get("phone", "")
            website = channel.get("website", "")
            desc = channel.get("description", "")

            lines.append(f"### {name}")
            lines.append("")
            if phone:
                lines.append(f"- **電話**: {phone}")
            if website:
                lines.append(f"- **網站**: [{website}]({website})")
            if desc:
                lines.append(f"- {desc}")
            lines.append("")

        return "\n".join(lines)

    def _render_recovery_section(self) -> str:
        """渲染追回流程區塊"""
        steps = self.data_loader.get_recovery_steps()
        lines = []

        lines.append("被騙後請依照以下步驟處理：")
        lines.append("")

        for step in steps:
            step_num = step.get("step", "")
            title = step.get("title", "")
            desc = step.get("description", "")

            lines.append(f"### 步驟 {step_num}：{title}")
            lines.append("")
            lines.append(desc)
            lines.append("")

        return "\n".join(lines)

    def _render_legitimacy(self, platform: ScamPlatform) -> str:
        """渲染合法性區塊"""
        lines = []

        if platform.platform_type == "scam_pattern":
            # 這是詐騙模式，不是平台
            lines.append(f"**{platform.chinese_name}是一種常見的詐騙手法**，而非合法的投資管道。")
            lines.append("")
            lines.append("這類詐騙通常具有以下特徵：")
            lines.append("")
            if platform.warning_signs:
                for sign in platform.warning_signs[:5]:
                    lines.append(f"- {sign}")
        elif platform.is_legit:
            lines.append(f"**{platform.name}本身是合法的{self._get_platform_type_name(platform.platform_type)}**。")
            lines.append("")

            if platform.taiwan_licensed:
                lines.append(f"- {platform.name} 擁有台灣金管會核准的虛擬通貨交易業者資格")
                if platform.license_info:
                    lines.append(f"- 牌照資訊：{platform.license_info}")
            else:
                lines.append(f"- {platform.name} 是國際知名的交易所，但**未在台灣取得牌照**")
                lines.append("- 使用時需自行承擔風險")

            lines.append("")
            lines.append(f"然而，詐騙集團經常**假冒{platform.name}的名義**進行詐騙，這就是我們常說的「{platform.chinese_name}詐騙」。")
            lines.append("")

            if platform.official_url:
                lines.append(f"**官方網站**: [{platform.official_url}]({platform.official_url})")
        else:
            lines.append(f"**{platform.name}存在安全疑慮**，請謹慎使用。")

        return "\n".join(lines)

    def _get_platform_type_name(self, platform_type: str) -> str:
        """取得平台類型的中文名稱"""
        type_names = {
            "taiwan_exchange": "台灣虛擬貨幣交易所",
            "international_exchange": "國際虛擬貨幣交易所",
            "stablecoin": "穩定幣",
            "scam_pattern": "詐騙模式"
        }
        return type_names.get(platform_type, "平台")


def render_scam_page(platform_id: str) -> Dict[str, str]:
    """便捷函式：渲染詐騙防範頁面"""
    renderer = ScamTemplateRenderer()
    return renderer.render(platform_id)


if __name__ == "__main__":
    # 測試
    renderer = ScamTemplateRenderer()

    print("=== 測試 BitoPro 渲染 ===")
    result = renderer.render("bitopro")

    print(f"標題: {result['metadata']['title']}")
    print(f"需要 LLM 填充的區塊: {result['placeholders']}")
    print("\n=== Markdown 預覽（前 2000 字）===")
    print(result['markdown'][:2000])

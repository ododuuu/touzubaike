"""
Scam Data Loader - 載入詐騙平台數據
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ScamType:
    name: str
    description: str

@dataclass
class ScamPlatform:
    id: str
    name: str
    chinese_name: str
    aliases: List[str]
    platform_type: str
    keywords: List[str]
    common_scam_types: List[ScamType]
    is_legit: bool
    official_url: Optional[str] = None
    taiwan_licensed: Optional[bool] = None
    license_info: Optional[str] = None
    warning_signs: Optional[List[str]] = None
    official_contact: Optional[Dict[str, str]] = None
    recovery_info: Optional[Dict] = None

class ScamDataLoader:
    """載入和管理詐騙平台數據"""

    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            # 預設路徑
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, "..", "data", "scam_platforms.json")

        self.data_path = data_path
        self._data = None
        self._platforms = {}

    def load(self) -> Dict:
        """載入 JSON 數據"""
        if self._data is None:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            self._index_platforms()
        return self._data

    def _index_platforms(self):
        """建立平台索引"""
        for platform in self._data.get("platforms", []):
            self._platforms[platform["id"]] = platform

    def get_platform(self, platform_id: str) -> Optional[ScamPlatform]:
        """取得單一平台資料"""
        self.load()
        raw = self._platforms.get(platform_id)
        if raw is None:
            return None

        scam_types = [
            ScamType(name=st["name"], description=st["description"])
            for st in raw.get("common_scam_types", [])
        ]

        return ScamPlatform(
            id=raw["id"],
            name=raw["name"],
            chinese_name=raw["chinese_name"],
            aliases=raw.get("aliases", []),
            platform_type=raw.get("type", "unknown"),
            keywords=raw.get("keywords", []),
            common_scam_types=scam_types,
            is_legit=raw.get("is_legit", False),
            official_url=raw.get("official_url"),
            taiwan_licensed=raw.get("taiwan_licensed"),
            license_info=raw.get("license_info"),
            warning_signs=raw.get("warning_signs"),
            official_contact=raw.get("official_contact"),
            recovery_info=raw.get("recovery_info")
        )

    def get_all_platforms(self) -> List[ScamPlatform]:
        """取得所有平台"""
        self.load()
        return [self.get_platform(pid) for pid in self._platforms.keys()]

    def get_platform_ids(self) -> List[str]:
        """取得所有平台 ID"""
        self.load()
        return list(self._platforms.keys())

    def get_report_channels(self, region: str = "taiwan") -> List[Dict]:
        """取得報案管道"""
        self.load()
        return self._data.get("common_report_channels", {}).get(region, [])

    def get_general_warning_signs(self) -> List[str]:
        """取得通用警示訊號"""
        self.load()
        return self._data.get("general_warning_signs", [])

    def get_recovery_steps(self) -> List[Dict]:
        """取得追回流程"""
        self.load()
        return self._data.get("recovery_general_steps", [])


def load_platform(platform_id: str) -> Optional[ScamPlatform]:
    """便捷函式：載入單一平台"""
    loader = ScamDataLoader()
    return loader.get_platform(platform_id)


def load_all_platforms() -> List[ScamPlatform]:
    """便捷函式：載入所有平台"""
    loader = ScamDataLoader()
    return loader.get_all_platforms()


if __name__ == "__main__":
    # 測試
    loader = ScamDataLoader()

    print("=== 所有平台 ID ===")
    print(loader.get_platform_ids())

    print("\n=== BitoPro 詳細資料 ===")
    bitopro = loader.get_platform("bitopro")
    if bitopro:
        print(f"名稱: {bitopro.name} ({bitopro.chinese_name})")
        print(f"類型: {bitopro.platform_type}")
        print(f"合法: {bitopro.is_legit}")
        print(f"台灣牌照: {bitopro.taiwan_licensed}")
        print(f"詐騙手法數: {len(bitopro.common_scam_types)}")
        for st in bitopro.common_scam_types:
            print(f"  - {st.name}: {st.description[:50]}...")

    print("\n=== 通用警示訊號 ===")
    for sign in loader.get_general_warning_signs()[:3]:
        print(f"  - {sign}")

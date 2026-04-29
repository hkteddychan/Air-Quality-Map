# 💨 Air Quality Map

香港分區空氣質量地圖 — 每小時自動從 Open-Meteo 更新。

## 數據源
- [Open-Meteo Air Quality API](https://open-meteo.com/) (免費，無需 API key)

## 覆蓋地區
中環、觀塘、荃灣、元朗、東涌、將軍澳

## 自動更新
GitHub Actions 每小時 :30 分執行

## AQI 等級
- 0-50: 良好 🟢
- 51-100: 中等 🟡
- 101-150: 敏感人士關注 🟠
- 151+: 不健康 🔴

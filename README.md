# 智慧門禁人臉辨識系統 (Face Recognition Access Control System)

---

## 📌 專案介紹

本專案為一套結合人臉辨識技術的智慧門禁系統，透過 Web 平台實現使用者註冊、照片上傳與管理員審核流程，並整合 AI 模型進行人臉辨識，達成自動化身份驗證。

系統同時串接 LINE Bot，於照片審核完成後即時通知使用者，提高系統即時性與互動體驗。

---

## 🚀 使用技術

### Frontend

* Vue.js
* Vuetify
* Axios

### Backend

* Node.js
* Express
* JWT（身份驗證）

### AI / Computer Vision

* YOLOv8（人臉偵測）
* ArcFace（人臉辨識）

### Database

* Supabase

### 系統與網路

* Nginx（反向代理）
* ngrok（外網穿透 / Webhook 測試）

---

## 🧩 系統功能

### 👤 使用者

* 註冊 / 登入
* 上傳人臉照片
* 查詢審核結果

### 🛠 管理員

* 使用者管理
* 照片審核（通過 / 拒絕）
* 紀錄查詢

### 🤖 AI 辨識

* YOLOv8：偵測影像中的人臉
* ArcFace：進行人臉特徵比對

### 📲 通知

* 透過 LINE Bot 發送審核結果

---

## 🏗 系統架構（Nginx Reverse Proxy）

本系統使用 Nginx 作為統一入口，並將不同請求路徑轉發至對應服務。

### 路由設計

| 路徑          | 對應服務     | Port |
| ----------- | -------- | ---- |
| `/`         | 前端 Vue   | 8080 |
| `/api/`     | 後端 API   | 3000 |
| `/linebot/` | LINE Bot | 5000 |
| `/image/`   | 圖片服務     | 8000 |

---

### 請求流程

```text
Client
  ↓
Nginx (Port 80)
  ├── /        → Vue (8080)
  ├── /api     → Node.js (3000)
  ├── /linebot → LINE Bot (5000)
  └── /image   → Image Server (8000)
```

---

## 🌐 ngrok（Webhook 外網存取）

由於 LINE Bot webhook 必須使用公開 URL，本專案使用 ngrok 將本地服務暴露至外網：

### 用途

* 將本地伺服器轉換為公開網址
* 提供 LINE Bot webhook 使用
* 支援多服務測試（API / 圖片）

⚠️ 注意：
目前 ngrok 使用付費網域功能，專案無法長期完整運行

---

## ⚙️ 專案執行說明

⚠️ 本專案部分功能依賴第三方服務（Supabase、LINE Messaging API、ngrok），目前因訂閱限制無法完整啟用。

但仍可透過程式碼了解系統架構與實作方式。

---

### 🧪 本地測試（部分功能）

#### Frontend

```bash
cd frontend
npm install
npm run serve
```

#### Backend

```bash
cd backend
npm install
node index.js
```

---

## 🔐 環境變數（範例）

```env
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
JWT_SECRET=your_secret
LINE_CHANNEL_ACCESS_TOKEN=your_token
LINE_CHANNEL_SECRET=your_secret
```

---

## 📂 專案結構

```text
project/
├── frontend/        # Vue 前端
├── backend/         # Node.js API / LINE Bot
├── uploads/         # 使用者圖片（已忽略）
├── README.md
```

---

## 📸 Demo（建議補上）

* 登入畫面
* 照片上傳
* 管理員審核頁面

---

## 💡 專案亮點（面試重點）

* 🔹 前後端分離架構（Vue + Node.js）
* 🔹 使用 Nginx 實現反向代理與單一入口
* 🔹 多服務整合（API / LINE Bot / 圖片服務）
* 🔹 整合 YOLOv8 + ArcFace 實現人臉辨識
* 🔹 使用 JWT 進行權限控管
* 🔹 串接 LINE Bot 提供即時通知
* 🔹 使用 ngrok 解決 webhook 外網需求

---

## 📈 未來優化

* 雲端部署（Vercel / Render）
* 即時影像串流辨識
* 權限管理強化（RBAC）
* 模型效能優化

---

## 👨‍💻 作者

* 陳耀銘

---

## 📎 GitHub

https://github.com/你的帳號/你的repo

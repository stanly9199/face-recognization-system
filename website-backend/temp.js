const express = require('express');
const multer = require('multer');
const path = require('path');
const cors = require('cors');
const fs = require('fs');
const jwt = require('jsonwebtoken');

// 引入 supabase-js
const { createClient } = require('@supabase/supabase-js');

const axios = require('axios');

//line-bot
const line = require('@line/bot-sdk');
const client = new line.Client({
    channelAccessToken: 'b8nOKxEmd1G+PCkDp4+SlMAJe6atx84R54xFcB9a+dE4YMkpU906DqH8w6ZNF9osAWPyqHEL7sRM5dggC43hzTVeps5fjYyW9Pz6ZWnz3hFHMPsxB/OsIJ8zSF0+MpMheBZIitYRtor/DcL1oaxrtQdB04t89/1O/w1cDnyilFU=s', // 替換成你的 Token
});

const dirname = '../../image/'

const uploadsDir = path.join(dirname, 'upload');
const verifyDir = path.join(dirname, 'verify');
const rejectDir = path.join(dirname, 'reject');

const app = express();
const port = 3000;

// 中間件
app.use(cors('https://lab305.ngrok.pro'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

 // 使用你的 Supabase API URL 和匿名金鑰
 const supabaseUrl = 'https://ldhkgewrbqvhipuvuuzy.supabase.co/'; // 替換成你的 Supabase URL
 const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxkaGtnZXdyYnF2aGlwdXZ1dXp5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNjQwODA3OSwiZXhwIjoyMDQxOTg0MDc5fQ.kPul3SBWekxBguHJXrDBCnnvgmsAOwBBrp7DPnFSZNs'; // 替換成你的 anon key

// // 創建 Supabase 客戶端
 const supabase = createClient(supabaseUrl, supabaseAnonKey);

 const jwtSecret = 'your_secret_key';

// Ensure 'upload' directory exists
const uploadDir = path.join(__dirname, '../../image/upload');
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

// Configure multer storage with custom naming convention
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadDir); // save in 'upload' folder
  },
  filename: (req, file, cb) => {
    const { name } = req.body; // Get the username
    const fileIndex = req.fileIndex || 1;
    req.fileIndex = fileIndex + 1; // Increment for each file
    cb(null, `${name}_${fileIndex}.jpg`); // Save as 'username_1.jpg', 'username_2.jpg', etc.
  }
});

const upload = multer({
  storage: storage,
  limits: { files: 5 } // Limit to 5 files
});

// Route to handle upload
app.post('/api/uploads', upload.array('photos', 5), (req, res) => {
  try {
    res.json({ success: true, message: 'Images uploaded successfully!' });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Image upload failed.', error });
  }
});



// 2. 用戶註冊
app.post('/api/register', async (req, res) => {
    const { username, email, password,lineId } = req.body;

    try {
        // 1. 檢查是否已存在相同的電子郵件
        const { data: existingUser, error: selectError } = await supabase
            .from('person')
            .select('email')
            .eq('email', email)
            .single();

        if (selectError && selectError.code !== 'PGRST116') {
            // 非空結果，說明存在錯誤
            throw selectError;
        }

        if (existingUser) {
            // 如果存在使用相同電子郵件的用戶，返回錯誤訊息
            return res.status(400).json({ message: '此電子郵件已被註冊' });
        }

        // 3. 如果電子郵件不存在，插入新用戶
        const { error } = await supabase
            .from('person')
            .insert([
                { name: username, email, password, permission: 'User',line_id:lineId },
            ]);

        if (error) {
            throw error;
        }

        // 3. 註冊成功，返回成功訊息
        res.status(201).json({ message: '註冊成功' });

    } catch (error) {
        console.error('註冊過程中出錯:', error);
        res.status(500).json({ message: '註冊過程中發生錯誤，請稍後再試。' });
    }
});

// 3.用戶登錄
app.post('/api/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        // 查找數據庫中是否存在該用戶
        const { data: users, error } = await supabase
            .from('person')
            .select('*')
            .or(`email.eq.${username},name.eq.${username}`); // 支持使用 email 或 username 進行查找

        if (error) {
            throw error;
        }

        // 檢查用戶是否存在
        if (users.length === 0) {
            return res.status(400).json({ message: '用戶不存在，請檢查您的電子郵件。' });
        }

        const user = users[0];

        // 直接比較密碼是否匹配，不加密
        if (user.password !== password) {
            return res.status(401).json({ message: '密碼錯誤，請再試一次。' });
        }

        // 創建 JWT token
        const token = jwt.sign({ userId: user.id, username: user.name }, jwtSecret, { expiresIn: '1h' });

        // 登錄成功
        res.json({
            message: '登錄成功',
            token,
            username: user.name, // 返回用戶名
            permission: user.permission ,// 返回用戶權限
            lineId:user.line_id
        });
    } catch (error) {
        console.error('登錄過程中出錯:', error);
        res.status(500).json({ message: '登錄過程中發生錯誤，請稍後再試。' });
    }
});


// 4. 獲取用戶列表（僅作示例，實際應用中應添加適當的權限控制）
// 返回所有用戶的路由
app.get('/api/users', async (req, res) => {
    try {
        const { data, error } = await supabase
            .from('person')
            .select('name, email, password, permission');
            
        if (error) {
            throw error;
        }

        res.json(data);
    } catch (error) {
        console.error('獲取用戶數據時出錯:', error);
        res.status(500).json({ message: '獲取用戶數據失敗。' });
    }
});

// 更新指定用戶的路由
app.put('/api/users/:email', async (req, res) => {
    const { email } = req.params;
    const { name, password, permission } = req.body;

    try {
        // 更新指定用戶的數據
        const { error } = await supabase
            .from('person')
            .update({ name, password, permission })
            .eq('email', email);

        if (error) {
            throw error;
        }

        res.status(200).json({ message: '更新成功' });
        console.log("successful to update")
    } catch (error) {
        console.error('更新用戶出錯:', error);
        res.status(500).json({ message: '更新失敗，請稍後再試。' });
    }
});

//6.紀錄顯示
app.get('/api/records', async (req, res) => {
    try {
      const { data, error } = await supabase.from('record').select('date, time, name, image');
  
      if (error) {
        console.error('Supabase error:', error);
        return res.status(500).json({ error: error.message });
      }
  
      //console.log('Fetched data:', data); // 打印查詢結果
      res.json(data);
    } catch (error) {
      console.error('Server error:', error);
      res.status(500).json({ error: '伺服器錯誤，無法查詢紀錄' });
    }
});

// 取得照片列表
app.get('/api/uploads', (req, res) => {
  fs.readdir(uploadsDir, (err, files) => {
    if (err) {
      return res.status(500).json({ message: '讀取照片失敗' });
    }
    // 過濾出圖片類型文件
    const imageFiles = files.filter((file) =>
      /\.(jpg|jpeg|png|gif)$/i.test(file)
    );
    res.json(imageFiles);
  });
});
  
// 處理照片移動
app.post('/api/movePhoto', (req, res) => {
  const { filename, destination } = req.body;

  if (!filename || !destination) {
    return res.status(400).json({ message: '缺少必要參數' });
  }

  const sourcePath = path.join(uploadsDir, filename);
  let targetDir;

  if (destination === 'verify') {
    targetDir = verifyDir;
  } else if (destination === 'reject') {
    targetDir = rejectDir;
  } else {
    return res.status(400).json({ message: '無效的目的地' });
  }

  const targetPath = path.join(targetDir, filename);

  // 確保目的地資料夾存在
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  // 移動文件
  fs.rename(sourcePath, targetPath, (err) => {
    if (err) {
      return res.status(500).json({ message: '移動照片失敗', error: err });
    }
    res.json({ message: '照片已移動', filename, destination });
  });
});

// Ensure directories exist
[uploadDir, verifyDir, rejectDir].forEach((dir) => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir);
});
  
// Ensure directories exist
[uploadDir, verifyDir, rejectDir].forEach((dir) => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir);
});
  
// Fetch photos for review
app.get('/api/photos', (req, res) => {
  try {
    const files = fs.readdirSync(uploadDir);
    res.json(files);
  } catch (error) {
    res.status(500).json({ success: false, message: '無法讀取照片目錄', error });
  }
});

// Approve or deny photos
app.post('/api/photoAction', async (req, res) => {
  const { photos, action, userId } = req.body;

  if (!photos || !photos.length || !['verify', 'reject'].includes(action)) {
    return res.status(400).json({ success: false, message: '無效的請求參數' });
  }

  const targetDir = action === 'verify' ? verifyDir : rejectDir;

  try {
    // Move files to the target directory
    for (const photo of photos) {
      const sourcePath = path.join(uploadDir, photo);
      const targetPath = path.join(targetDir, photo);

      if (fs.existsSync(sourcePath)) {
        fs.renameSync(sourcePath, targetPath); // Move the file

        if (action === 'verify') {
          // Add approved photo to the database
          await supabase.from('recognition').insert({
            name: userId,
            image: photo,
          });
        }
      }
    }

    // Notify via Line Bot
    await notifyUsers(userId, action, photos.length);

    res.json({ success: true, message: '照片已成功處理' });
  } catch (error) {
    console.error('Error processing photos:', error);
    res.status(500).json({ success: false, message: '無法處理照片', error });
  }
});

// Notify users and admins via Line Bot
async function notifyUsers(userId, action, photoCount) {
  try {
    // Get the user's Line ID from the database
    const { data: user, error: userError } = await supabase
      .from('person')
      .select('line_id')
      .eq('name', userId)
      .single();

    if (userError || !user) {
      throw new Error('無法找到用戶的 Line ID');
    }

    const userLineId = user.line_id;

    // Get all admins' Line IDs
    const { data: admins, error: adminError } = await supabase
      .from('person')
      .select('line_id')
      .eq('permission', 'Admin');

    if (adminError) {
      throw new Error('無法找到管理員的 Line ID');
    }

    const adminLineIds = admins.map((admin) => admin.line_id);

    // Create notification message
    const message =
      action === 'verify'
        ? `✅ ${photoCount} 張照片已通過審核。`
        : `❌ ${photoCount} 張照片已被拒絕。`;

    // Notify the user
    await lineClient.pushMessage(userLineId, {
      type: 'text',
      text: message,
    });

    // Notify all admins
    const adminMessages = adminLineIds.map((lineId) =>
      lineClient.pushMessage(lineId, {
        type: 'text',
        text: `用戶 ${userId} 的照片已處理：${message}`,
      })
    );

    await Promise.all(adminMessages);
  } catch (error) {
    console.error('通知失敗:', error);
  }
}



// 啟動服務器
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
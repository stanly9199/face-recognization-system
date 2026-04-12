require('dotenv').config();
const express = require('express');
const multer = require('multer');
const path = require('path');
const cors = require('cors');
const fs = require('fs');
const jwt = require('jsonwebtoken');
const { createClient } = require('@supabase/supabase-js');
const line = require('@line/bot-sdk');
const axios = require('axios');

const app = express();
const port = 3000;

// Directory paths
const imageDir = path.resolve(__dirname, '../../image');
const uploadDir = path.join(imageDir, 'upload');
const verifyDir = path.join(imageDir, 'verify');
const rejectDir = path.join(imageDir, 'reject');

// Supabase setup
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);

// Line bot setup
const lineClient = new line.Client({ channelAccessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN });
const line_token = process.env.LINE_CHANNEL_ACCESS_TOKEN;

// JWT secret
const jwtSecret = process.env.JWT_SECRET;

// Middleware
app.use(cors({ origin: 'https://lab305.ngrok.pro' }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Ensure directories exist
[uploadDir, verifyDir, rejectDir].forEach((dir) => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

// Multer storage configuration
const storage = multer.diskStorage({
  limits: {
    fileSize: 50 * 1024 * 1024 // 10 MB limit
  },
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    const { name } = req.body;
    req.fileIndex = req.fileIndex ? req.fileIndex + 1 : 1;
    cb(null, `${name}_${req.fileIndex}.jpg`);
  },
});
const upload = multer({ storage, limits: { files: 5 } });

// Helper function to save image numbers to Supabase
async function saveImageNumbers(userId, approvedImages = [], rejectedImages = []) {
  try {
    const { data: record, error: fetchError } = await supabase
      .from('recognition')
      .select('image, reject')
      .eq('name', userId)
      .single();

    if (fetchError && fetchError.code !== 'PGRST116') {
      console.error('Error fetching user record:', fetchError);
      return;
    }

    const existingImages = record?.image ? record.image.split(',').map(Number) : [];
    let existingRejected = record?.reject ? record.reject.split(',').map(Number) : [];

    // Add approved images to image column
    approvedImages.forEach((image) => {
      const imageNumber = +image.split('_')[1].split('.')[0];
      if (!existingImages.includes(imageNumber)) {
        existingImages.push(imageNumber);
      }
      // Remove the approved number from the reject column if it exists
      existingRejected = existingRejected.filter((num) => num !== imageNumber);
    });

    // Add rejected images to reject column
    rejectedImages.forEach((image) => {
      const imageNumber = +image.split('_')[1].split('.')[0];
      if (!existingRejected.includes(imageNumber)) {
        existingRejected.push(imageNumber);
      }
    });

    const updatedImages = existingImages.sort((a, b) => a - b).join(',');
    const updatedRejected = existingRejected.sort((a, b) => a - b).join(',');

    if (record) {
      const { error: updateError } = await supabase
        .from('recognition')
        .update({ image: updatedImages, reject: updatedRejected })
        .eq('name', userId);

      if (updateError) console.error('Error updating record:', updateError);
    } else {
      const { error: insertError } = await supabase
        .from('recognition')
        .insert({ name: userId, image: updatedImages, reject: updatedRejected });

      if (insertError) console.error('Error inserting new record:', insertError);
    }
  } catch (error) {
    console.error('Error saving image numbers:', error);
  }
}



// Helper function to notify users and admins
async function notifyUsersAndAdmins(userId, action, approved, rejected) {
  try {
    const { data: user, error: userError } = await supabase
      .from('person')
      .select('line_id')
      .eq('name', userId)
      .single();

    if (userError || !user) {
      console.error('Error fetching user Line ID:', userError || 'User not found');
      return;
    }

    const { data: admins, error: adminError } = await supabase
      .from('person')
      .select('line_id')
      .eq('permission', 'Admin');

    if (adminError) {
      console.error('Error fetching admin Line IDs:', adminError);
      return;
    }

    const rejected_num = rejected.map(file => +file.split('_')[1].split('.')[0]);
    userMessage = ''
    if ((action === 'verify' && approved.length == 5)) {
      userMessage = `✅ 您的所有照片皆被批准`;
      const { error } = await supabase
        .from('person')
        .update({ permission: 'Member' })
        .eq('name', userId);
      if (userError || !user) {
        console.error('Error changing permission:', error);
        return;
      }
    }
    else if (action === 'reject')
      userMessage = `❌ 您的照片遭到拒絕\n編號: ${rejected_num}`;

    // const adminMessage = `User ${userId}'s photos: ${userMessage}`;

    if (user.line_id) {
      await axios.post(
        'https://api.line.me/v2/bot/message/push',
        {
          to: user.line_id,
          messages: [{ type: 'text', text: userMessage }],
        },
        {
          headers: { Authorization: `Bearer ${line_token}` },
        }
      );
      console.log(`Notified user ${userId} successfully`);
    }

    // const adminNotifications = admins.map(async (admin) => {
    //   if (admin.line_id) {
    //     await axios.post(
    //       'https://api.line.me/v2/bot/message/push',
    //       {
    //         to: admin.line_id,
    //         messages: [{ type: 'text', text: adminMessage }],
    //       },
    //       {
    //         headers: { Authorization: `Bearer ${line_token}` },
    //       }
    //     );
    //     console.log(`Notified admin ${admin.line_id} successfully`);
    //   } else {
    //     console.log('Admin missing Line ID, notification skipped');
    //   }
    // });

    // await Promise.all(adminNotifications);
    console.log('All notifications sent');
  } catch (err) {
    console.error('Error during notifications:', err);
  }
}

// Routes

// Upload route
app.post('/api/uploads', upload.array('photos', 5), (req, res) => {
  res.json({ success: true, message: 'Images uploaded successfully!' });
});

// Approve or deny photos
app.post('/api/photoAction', async (req, res) => {
  const { photos, action } = req.body;
  if (!photos || !['verify', 'reject'].includes(action)) {
      return res.status(400).json({ success: false, message: 'Invalid request parameters' });
  }

  const targetDir = action === 'verify' ? verifyDir : rejectDir;
  const approvedImages = [];
  const rejectedImages = [];

  try {
      const userId = photos[0].split('_')[0];

      for (const photo of photos) {
          const sourcePath = path.join(uploadDir, photo);
          const targetPath = path.join(targetDir, photo);

          if (fs.existsSync(sourcePath)) {
              fs.renameSync(sourcePath, targetPath);

              if (action === 'verify') {
                  approvedImages.push(photo);
              } else if (action === 'reject') {
                  rejectedImages.push(photo);
              }
          }
      }

      await saveImageNumbers(userId, approvedImages, rejectedImages);
      await notifyUsersAndAdmins(userId, action, approvedImages, rejectedImages);
      res.json({ success: true, message: 'Photos processed successfully' });
  } catch (error) {
      console.error('Photo processing error:', error);
      res.status(500).json({ success: false, message: 'Unable to process photos', error });
  }
});


// User registration
app.post('/api/register', async (req, res) => {
    const { username, email, password, lineId } = req.body;
    try {
        const { data: existingUser } = await supabase
        .from('person')
        .select('email')
        .eq('email', email)
        .single();
        if (existingUser) return res.status(400).json({ message: 'Email already registered' });

        await supabase.from('person').insert({ name: username, email, password, permission: 'User', line_id: lineId });
        res.status(201).json({ message: 'Registration successful' });
    } catch (error) {
        console.error('Registration error:', error);
        res.status(500).json({ message: 'An error occurred. Please try again.' });
    }
});

// User login
app.post('/api/login', async (req, res) => {
const { username, password } = req.body;
    try {
        const { data: users } = await supabase
        .from('person')
        .select('*')
        .or(`email.eq.${username},name.eq.${username}`);
        if (!users.length) return res.status(400).json({ message: 'User not found' });

        const user = users[0];
        if (user.password !== password) return res.status(401).json({ message: 'Invalid password' });

        const token = jwt.sign({ userId: user.id, username: user.name }, jwtSecret, { expiresIn: '1h' });
        res.json({ message: 'Login successful', token, username: user.name, permission: user.permission, lineId: user.line_id });
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ message: 'An error occurred. Please try again.' });
    }
});

// Get photos for review
app.get('/api/photos', (req, res) => {
    try {
        const files = fs.readdirSync(uploadDir).filter((file) => /\.(jpg|jpeg|png)$/i.test(file));
        res.json(files);
    } catch (error) {
        console.error('Error reading upload directory:', error);
        res.status(500).json({ success: false, message: 'Unable to read photo directory' });
    }
});

//record
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

//user
app.get('/api/users', async (req, res) => {
  try {
      const { data, error } = await supabase
          .from('person')
          .select('ID, name, email, password, permission');
          
      if (error) {
          throw error;
      }

      res.json(data);
  } catch (error) {
      console.error('獲取用戶數據時出錯:', error);
      res.status(500).json({ message: '獲取用戶數據失敗。' });
  }
});

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

// Start server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

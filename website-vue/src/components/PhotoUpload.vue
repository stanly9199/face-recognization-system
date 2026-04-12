  <template>
    <div class="photo-upload">
      <h2>上傳照片</h2>
      <div 
        class="upload-area" 
        @click="triggerFileInput" 
        @dragover.prevent 
        @drop.prevent="handleDrop"
      >
        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileChange" 
          accept="image/*" 
          multiple  
          style="display: none;"
        >
        <p v-if="!imagePreviews.length">點擊或拖拽照片到這裡上傳</p>
        <div v-if="imagePreviews.length" class="preview-images">
          <img v-for="(preview, index) in imagePreviews" :key="index" :src="preview" alt="Preview" class="preview-image">
        </div>
      </div>
      <button @click="uploadPhotos" :disabled="!selectedFiles.length">上傳</button>
      <span class="upload-text" v-if="uploadStatus">{{ uploadStatus }}</span>
      
      
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { BASE_URL } from '../main';
  
  export default {
    name: 'PhotoUpload',
    setup() {
      const fileInput = ref(null);
      const selectedFiles = ref([]);  // 用於存儲選擇的文件
      const imagePreviews = ref([]);   // 用於存儲圖片預覽
      const uploadStatus = ref('');
  
      const triggerFileInput = () => {
        fileInput.value.click();
      };
  
      const handleFileChange = (event) => {
        const files = Array.from(event.target.files);
        handleFiles(files);
      };
  
      const handleDrop = (event) => {
        const files = Array.from(event.dataTransfer.files);
        handleFiles(files);
      };
  
      const handleFiles = (files) => {
        const totalFiles = selectedFiles.value.length + files.length;
        if (totalFiles != 5) {
          alert('請上傳5張照片');
          return;
        }

        files.forEach(file => {
          if (file && file.type.startsWith('image/')) {
            selectedFiles.value.push(file);
            const reader = new FileReader();
            reader.onload = (e) => {
              imagePreviews.value.push(e.target.result);
            };
            reader.readAsDataURL(file);
          } else {
            alert('請選擇一個或多個圖片文件');
          }
        });
      };


      const uploadPhotos = async () => {
        if (!selectedFiles.value.length) return;

          const formData = new FormData();
          formData.append('name', localStorage.getItem('username')); // 添加用戶名
          selectedFiles.value.forEach(file => {
          formData.append('photos', file); // 使用 'photos' 作為鍵
        });

    // 獲取用戶名稱並添加到 FormData
      // const username = localStorage.getItem('username'); // 獲取用戶名稱
      // console.log('uploading files for user:', username); // 檢查用戶名稱
      // formData.append('name', username); // 將用戶名稱添加到 FormData


    // 在這裡打印 FormData 的內容
      for (let [key, value] of formData.entries()) {
        console.log(key, value);
      }
    
      uploadStatus.value = '上傳中...';

      try {
        // const response = await fetch('http://192.168.10.11:3000/uploads', {
        //   method: 'POST',
        //   body: formData
        // });
        const response = await fetch(`${BASE_URL}/api/uploads`, {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error('Upload failed');
        }

        const result = await response.json();
        uploadStatus.value = '上傳成功！';
          console.log('Uploaded files:', result);

        // 重置狀態
        selectedFiles.value = [];
        imagePreviews.value = [];
      } catch (error) {
        console.error('Error:', error);
        uploadStatus.value = '上傳失敗，請重試。';
      }
    };

  
      return {
        fileInput,
        selectedFiles,
        imagePreviews,
        uploadStatus,
        triggerFileInput,
        handleFileChange,
        handleDrop,
        uploadPhotos
      };
    }
  };
  </script>
  
  <style scoped>
  /* 样式保持不变 */
  .preview-images {
    display: flex;
    flex-wrap: wrap;
  }
  .preview-image {
    max-width: 100px;
    max-height: 100px;
    margin: 5px;
  }
  .photo-upload {
    max-width: 500px;
    margin: 0 auto;
  }
  
  .upload-area {
    border: 2px dashed #ccc;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    margin-bottom: 20px;
  }
  
  .upload-area:hover {
    border-color: #888;
  }
  
  .preview-image {
    max-width: 100%;
    max-height: 300px;
  }
  
  button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-bottom: 10px;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  .upload-text {
    margin-left: 15px;
  }

</style>
  
  
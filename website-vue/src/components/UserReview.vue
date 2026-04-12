
<!-- <template>
  <div>
    <h1>照片審核</h1>
    <div v-if="photos.length">
      <div class="photo-grid">
        <div v-for="(photo, index) in photos" :key="index" class="photo-item">
          <img :src="`https://lab305.ngrok.pro/image/upload/${photo}`" :alt="photo" class="photo" />
          <p>{{ photo }}</p>
          <input type="checkbox" :value="photo" v-model="selectedPhotos" />
        </div>
      </div>
      <div class="action-buttons">
        <button @click="handlePhotoAction('verify')" :disabled="!selectedPhotos.length">
          批准選中的照片
        </button>
        <button @click="handlePhotoAction('reject')" :disabled="!selectedPhotos.length">
          拒絕選中的照片
        </button>
      </div>
    </div>
    <div v-else>
      <p>目前沒有需要審核的照片。</p>
    </div>
  </div>
</template> -->
<template>
  <div>
    <h1>照片審核</h1>
    <div v-if="photos.length">
      <div class="photo-grid">
        <div 
          v-for="(photo, index) in photos" 
          :key="index" 
          class="photo-item" 
          :class="{'selected': selectedPhotos.includes(photo)}"
        >
          <label class="photo-label">
            <img 
              :src="`https://lab305.ngrok.pro/image/upload/${photo}`" 
              :alt="photo" 
              class="photo" 
            />
            <p>{{ photo }}</p>
            <input 
              type="checkbox" 
              :value="photo" 
              v-model="selectedPhotos" 
              class="hidden-checkbox"
            />
          </label>
        </div>
      </div>
      <div class="action-buttons">
        <button class="left" @click="handlePhotoAction('verify')" :disabled="!selectedPhotos.length">
          批准選中的照片
        </button>
        <button class="right" @click="handlePhotoAction('reject')" :disabled="!selectedPhotos.length">
          拒絕選中的照片
        </button>
      </div>
    </div>
    <div v-else>
      <p>目前沒有需要審核的照片。</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BASE_URL } from '@/main';

export default {
  data() {
    return {
      photos: [], // 照片列表
      selectedPhotos: [], // 被選中的照片
    };
  },
  created() {
    this.fetchPhotos();
  },
  methods: {
    async fetchPhotos() {
      try {
        const response = await axios.get(`${BASE_URL}/api/photos`);
        this.photos = response.data;
      } catch (error) {
        console.error('無法獲取照片:', error);
      }
    },
    async handlePhotoAction(action) {
      if (!this.selectedPhotos.length) return;

      try {
        const response = await axios.post(`${BASE_URL}/api/photoAction`, {
          photos: this.selectedPhotos,
          action, // "verify" 或 "reject"
        });

        if (response.data.success) {
          // 移除已處理的照片
          this.photos = this.photos.filter((photo) => !this.selectedPhotos.includes(photo));
          this.selectedPhotos = [];
        } else {
          console.error('動作失敗:', response.data.message);
        }
      } catch (error) {
        console.error('動作請求失敗:', error);
      }
    },
  },
};
</script>


<!-- <style scoped>
  .user-review {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }

  .photo-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    position: relative; /* Ensures border is placed correctly */
  }
  .hidden-checkbox {
    display: none;
  }
  .photo-label img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    transition: border 0.3s, box-shadow 0.3s; /* Smooth transition for border */
  }
  .photo-label input:checked + img {
    border: 5px solid #e6a65d; /* Green border for selected images */
    box-shadow: 0 0 15px rgba(76, 175, 80, 0.7); /* Soft green glow effect */
  }

  .photo-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr); /* Adjust the number of columns as needed */
    gap: 10px;
    justify-items: center; /* Center items horizontally */
    align-items: center;   /* Center items vertically */
  } 
  .photo-item {
    display: flex;
    flex-direction: column;
    align-items: center; /* Center content horizontally */
    justify-content: center; /* Center content vertically */
  }
  .photo {
    max-width: 100%;
    height: auto;
    margin-bottom: 5px;
  }

  .photo-item img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    cursor: pointer;
  }

  .photo-info {
    padding: 10px;
    display: flex;
    align-items: center;
  }

  .photo-info input[type="checkbox"] {
    margin-right: 30px;
  }

  .action-buttons {
    display: flex;
    justify-content:space-evenly;
    margin-top: 20px;
  }

  button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:disabled {
    background-color: #ddd;
    cursor: not-allowed;
  }

  button:last-child {
    background-color: #f44336;
  }

  .success {
    color: green;
  }

  .error {
    color: red;
  }

</style> -->
<style scoped>
  .photo-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr); /* Adjust the number of columns as needed */
    gap: 10px;
    justify-items: center; /* Center items horizontally */
    align-items: center;   /* Center items vertically */
  }

  .photo-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 10px; /* Add padding to prevent the border from overlapping the image */
    box-sizing: border-box; /* Include padding and border in the element's size */
    height: 250px; /* Set a fixed height to avoid vertical movement */
  }

  .photo-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    position: relative;
    width: 100%;
  }

  .hidden-checkbox {
    display: none;
  }

  .photo-label img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    transition: border 0.3s, box-shadow 0.3s; /* Smooth transition for border */
    box-sizing: border-box; /* Include border in the image's size */
  }

  /* This class will be added when the image is selected */
  .photo-item.selected img {
    border: 5px solid #e6a65d; /* Border color for selected images */
    box-shadow: 0 0 15px rgba(230, 166, 93, 0.7); /* Soft yellow glow effect */
  }

  .action-buttons {
    display: flex;
    justify-content: space-evenly;
    margin-top: 20px;
  }

  button {
    color: #fff; /* White text color */
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease; /* Smooth transition for hover effect */
  }

  /* Disabled button styling */
  button:disabled {
    background-color: #ccc; /* Gray background when disabled */
    color: #fff; /* Lighter text color when disabled */
    cursor: not-allowed; /* Show not-allowed cursor */
  }

  /* Button styles for left and right buttons */
  .action-buttons .left {
    background-color: #4CAF50; /* Green background for 'verify' */
  }

  .action-buttons .right {
    background-color: #f44336; /* Red background for 'reject' */
  }

  /* Disabled state for specific buttons */
  .action-buttons .left:disabled {
    background-color: #c8e6c9; /* Lighter green for disabled */
  }

  .action-buttons .right:disabled {
    background-color: #ffcdd2; /* Lighter red for disabled */
  }

  /* Add hover effect for enabled buttons */
  button:not(:disabled):hover {
    opacity: 0.8;
  }
</style>
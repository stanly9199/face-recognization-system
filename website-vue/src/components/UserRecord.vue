<template>
  <div class="records">
    <h2>紀錄列表</h2>

    <!-- 添加日期区间筛选 -->
    <div class="filters">
      <label for="start-date">開始日期：</label>
      <input type="date" v-model="startDate" id="start-date" />
      
      <label for="end-date">結束日期：</label>
      <input type="date" v-model="endDate" id="end-date" />

      <button @click="filterRecords">篩選</button>
    </div>

    <div v-for="record in filteredRecords" :key="record.id" class="record">
      <p>日期：{{ record.date }}</p>
      <p>時間：{{ record.time }}</p>
      <p>名稱：{{ record.name }}</p>
      <img :src="getImageUrl(record.image)" alt="紀錄照片" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BASE_URL } from '../main';
import { IMAGE_URL } from '../main';

export default {
  data() {
    return {
      records: [],      // 所有记录
      filteredRecords: [], // 筛选后的记录
      startDate: '',    // 用户选择的开始日期
      endDate: '',      // 用户选择的结束日期
    };
  },
  methods: {
    async fetchRecords() {
      try {
        const response = await axios.get(`${BASE_URL}/api/records`);
        if (response.status !== 200) {
          console.error('API 回應錯誤:', response.statusText);
          throw new Error('查詢失敗');
        }
        this.records = response.data;

        // 假设 records 数据中有 date 字段用于排序
        // 按日期排序后选取最近的10笔记录
        this.records.sort((a, b) => new Date(b.date) - new Date(a.date));
        this.filteredRecords = this.records.slice(0, 10);  // 默认显示最近10笔记录
      } catch (error) {
        console.error('Fetch error:', error);
        alert('查詢失敗');
      }
    },

    filterRecords() {
      // 筛选逻辑：如果有日期区间，按区间过滤
      let filtered = this.records;

      if (this.startDate) {
        filtered = filtered.filter(record => 
          new Date(record.date).toISOString().split('T')[0] >= this.startDate
        );
      }

      if (this.endDate) {
        filtered = filtered.filter(record => 
          new Date(record.date).toISOString().split('T')[0] <= this.endDate
        );
      }

      this.filteredRecords = filtered;  // 更新筛选后的记录
      alert('查詢成功 ! ! !')
    },

    getImageUrl(imageName) {
      return `${IMAGE_URL}/record/image_${imageName}.jpg`;
    },
  },
  mounted() {
    this.fetchRecords();  // 获取记录数据
  },
};
</script>

<style scoped>
.records {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.record {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
  margin-top: 10px;
}

.filters {
  margin-bottom: 20px;
}

.filters label {
  margin-right: 10px;
}

.filters input {
  margin-right: 10px;
}
</style>
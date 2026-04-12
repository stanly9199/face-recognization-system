<template>
  <div>
    <h1>人員管理</h1>
    <table>
      <thead>
        <tr>
          <th>名稱</th>
          <th>電子郵件</th>
          <th>密碼</th>
          <th>權限</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="person in people" :key="person.email">
          <!-- 名稱輸入框 -->
          <td class="cell">
            <input v-model="person.name" />
          </td>
          <!-- 電子郵件輸入框 -->
          <td class="cell">
            <input v-model="person.email" disabled />
          </td>
          <!-- 密碼輸入框與顯示/隱藏按鈕 -->
          <td class="cell">
            <div class="password-container">
              <input 
                :type="person.showPassword ? 'text' : 'password'" 
                v-model="person.password" 
              />
              <button @click="togglePasswordVisibility(person)">
                {{ person.showPassword ? '隱藏' : '顯示' }}
              </button>
            </div>
          </td>
          <!-- 權限選擇框 -->
          <td class="cell">
            <select v-model="person.permission">
              <option value="User">User</option>
              <option value="Member">Member</option>
              <option value="Admin">Admin</option>
              <option value="Blocked">Blocked</option>
            </select>
          </td>
          <!-- 更新按鈕 -->
          <td class="center">
            <button @click="updatePerson(person)">更新</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<!-- <script>
// 引入 fetchPeople 和 updatePerson 方法
// import { fetchPeople, updatePerson } from '../supabase'; 

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://ldhkgewrbqvhipuvuuzy.supabase.co/';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxkaGtnZXdyYnF2aGlwdXZ1dXp5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY0MDgwNzksImV4cCI6MjA0MTk4NDA3OX0.4dlWl17gdGWU0T07ouG-IJvy4UyyYCzvXpQpM1x_W5o';
const supabase = createClient(supabaseUrl, supabaseKey);

// export default supabase;

export async function fetchPeople() {
  let { data, error } = await supabase
    .from('person')
    .select('name, email, password, permission');

  if (error) {
    console.error(error);
    return [];
  }

  return data;
}

export async function updatePerson(person) {
  const { name, email, password, permission } = person;

  let { data, error } = await supabase
    .from('person')
    .update({ name, email, password, permission })
    .eq('email', email);

  if (error) {
    console.error(error);
  } else {
    console.log('更新成功:', data);
  }
}

export default {
  data() {
    return {
      people: []
    };
  },
  async mounted() {
    // 從 Supabase 獲取人員資料
    this.people = await fetchPeople();
  },
  methods: {
    async updatePerson(person) {
      try {
        await updatePerson(person);
        alert('更新成功！');
      } catch (error) {
        console.error('更新失敗:', error);
        alert('更新失敗，請檢查控制台。');
      }
    }
  }
};
</script> -->

<script>
import axios from 'axios'; // 引入 axios
import { BASE_URL } from '../main';

export default {
  data() {
    return {
      people: []
    };
  },
  async mounted() {
    // 從 Supabase 獲取人員資料
    this.people = await this.fetchPeople();
  },
  methods: {
    // 獲取人員信息
    async fetchPeople() {
      try {
        //const response = await axios.get('http://192.168.10.11:3000/users');
        const response = await axios.get(`${BASE_URL}/api/users`);
        return response.data;
      } catch (error) {
        console.error('獲取人員數據失敗:', error);
        return [];
      }
    },

    // 更新指定人員信息
    async updatePerson(person) {
      try {
        await axios.put(`${BASE_URL}/api/users/${person.email}`, person);
        alert('更新成功！');
        // window.location.reload();
      } catch (error) {
        console.error('更新失敗:', error);
        alert('更新失敗，請檢查控制台。');
      }
    },
    togglePasswordVisibility(person) {
      person.showPassword = !person.showPassword;
    }
  }
};
</script>

<style scoped>
/* 表格樣式 */
table {
  width: 100%;
  border-collapse: collapse;
}

/* 單元格樣式 */
th,
td {
  border: 1px solid black;
  padding: 5px;
  text-align: center;
}

/* 輸入框與選單樣式 */
td.cell input,
td.cell select {
  width: 90%;
  height: 90%;
  box-sizing: border-box;
  padding: 5px;
  font-size: inherit;
}

/* 密碼容器樣式 */
.password-container {
  display: flex;
  align-items: center;
  gap: 5px;
}

.password-container input {
  flex: 1;
}

.password-container button {
  padding: 3px 8px;
  font-size: 0.9em;
  cursor: pointer;
}

/* 按鈕置中 */
.center button {
  width: 80%;
  padding: 5px 10px;
  cursor: pointer;
}
</style>

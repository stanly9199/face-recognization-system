
<template>
  <div class="sidebar-content">
    <div class="menu-items">
      <button @click="$emit('component-change', 'PhotoUpload')">上傳照片</button>
      <button @click="$emit('component-change', 'UserReview')">審核照片</button>
      <button @click="$emit('component-change', 'UserStaff')">人員管理</button>
      <button @click="$emit('component-change', 'UserRecord')">紀錄顯示</button>
    </div>
    <div class="auth-buttons">
      <button v-if="username" @click="logoutUser">登出</button>
      <button v-else @click="$emit('component-change', 'UserLogin')">登入</button>
      <button v-if="!username" @click="$emit('component-change', 'UserRegister')">註冊</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserSidebar',
  data() {
    return {
      username: null
    };
  },
  mounted() {
    // 在掛載組件時檢查 localStorage 中是否有 username
    this.username = localStorage.getItem('username');
  },
  methods: {
    logoutUser() {
      // 清除 localStorage 中的 token 和 username
      localStorage.removeItem('userToken');
      localStorage.removeItem('username');
      localStorage.removeItem('permission');
      localStorage.removeItem('line_id');
      this.username = null;
      location.reload();
      this.$emit('component-change', 'UserLogin'); // 導向登入頁面
    }
  }
};
</script>

<style scoped>
.sidebar-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: fixed;
  width: 200px;
}

.user-info {
  padding: 10px;
}

.menu-items {
  flex-grow: 1;
}

.menu-items button, .auth-buttons button {
  width: 90%;
  padding: 10px;
  margin-bottom: 5px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  margin-left: 10px;
}

.auth-buttons {
  padding: 10px;
  width:90%;
}
</style>


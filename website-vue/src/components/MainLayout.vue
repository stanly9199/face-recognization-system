
<template>
  <div class="app-container">
    <div class="sidebar">
      <UserSidebar @component-change="changeComponent" />
    </div>
    <div class="content">
      <component :is="activeComponent" @login-success="updateUsername"></component>
    </div>
    <UserHeader :username="username" @logged-out="handleLogout" />
  </div>
</template>

<script>
import PhotoUpload from './PhotoUpload.vue'
import UserLogin from './UserLogin.vue'
import UserRegister from './UserRegister.vue'
import UserReview from './UserReview.vue'
import UserStaff from './UserStaff.vue'
import UserSidebar from './UserSidebar.vue'
import UserHeader from './UserHeader.vue'
import UserRecord from './UserRecord.vue'

export default {
  name: 'MainLayout',
  components: {
    PhotoUpload,
    UserLogin,
    UserRegister,
    UserReview,
    UserStaff,
    UserSidebar,
    UserHeader,
    UserRecord
  },
  data() {
    return {
      activeComponent: 'UserLogin', // 預設顯示的組件
      username: null // 管理使用者名稱
    };
  },
  created() {
    // 初始化時檢查 localStorage 中是否有 username
    this.username = localStorage.getItem('username');
     // 如果有用戶名，切換到上傳組件
     if (this.username) {
      this.activeComponent = 'PhotoUpload';
    }
  },
  // methods: {
  //   changeComponent(componentName) {
  //     this.activeComponent = componentName;
  //   },
  //   handleLogout() {
  //     // 清空 username 並顯示登入頁面
  //     this.username = null;
  //     localStorage.removeItem('username');
  //     localStorage.removeItem('permission');
  //     localStorage.removeItem('line_id');
  //     this.activeComponent = 'UserLogin';
  //     location.reload();
  //   }
  // }
  
  methods: {
    changeComponent(componentName) {
      const permission = localStorage.getItem('permission');
      const adminComponents = ['UserReview', 'UserStaff', 'UserRecord'];
      
      // 如果尚未登入，僅允許進入登入和註冊頁面
      if (!this.username && componentName !== 'UserLogin' && componentName !== 'UserRegister') {
        alert('請先登入');
        this.activeComponent = 'UserLogin';
        return;
      }

      // 限制只有 Admin 權限的使用者可以查看的頁面
      if (adminComponents.includes(componentName) && permission !== 'Admin') {
        alert('您無權限訪問此頁面');
        return;
      }

      // 若有權限，切換組件
      this.activeComponent = componentName;
    },

    handleLogout() {
      this.username = null;
      localStorage.removeItem('username');
      localStorage.removeItem('permission');
      localStorage.removeItem('line_id');
      this.activeComponent = 'UserLogin';
      location.reload();
    }
  }

}
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #f0f0f0;
  position: fixed;
  height: 100%;
}

.content {
  flex-grow: 1;
  margin-left: 200px;
  padding: 20px;
  width: max-content;
}
</style>





















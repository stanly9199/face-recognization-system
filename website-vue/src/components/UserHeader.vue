
  <template>
    <div class="header-content">
      <span class="username">
        {{ username ? `歡迎, ${username}` : '訪客' }}
      </span>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UserHeader',
    //props: ['username'], // 從父組件接收 username 屬性
    props: {
    username: {
      type: String,
      default: ''
    }
  },
    methods: {
      logout() {
        this.$emit('logged-out'); // 通知父組件進行登出處理
      } 
    }
  }
  </script>
  
  <style scoped>
  .header-content {
    position: fixed;
    top: 0;
    right: 0;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    padding: 10px;
    background-color: #f0f0f0;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 1000;
  }
  
  .username {
    margin-right: 10px;
  }
  
  .logout-button {
    padding: 5px 10px;
    background-color: #FF5722;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>
  
  
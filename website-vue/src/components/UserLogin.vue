  <template>
    <div class="user-login">
      <h2>用戶登錄</h2>
      <form @submit.prevent="loginUser">
        <div class="form-group">
          <label for="username">電子郵件：</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required
          >
        </div>
        
        <div class="form-group">
          <label for="password">密碼：</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required
          >
        </div>
        
        <button type="submit" :disabled="!isFormValid">登入</button>
      </form>
      <p v-if="loginMessage" :class="{ 'success': loginSuccess, 'error': !loginSuccess }">
        {{ loginMessage }}
      </p>
    </div>
  </template>
  
<script>
  import { BASE_URL } from '@/main';
  export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: '',
      loginMessage: '',
      loginSuccess: false,
      isLoading: false,
      retryCount: 0,
      maxRetries: 3,
      networkStatus: true
    }
  },
  computed: {
    isFormValid() {
      return this.username && this.password;
    }
  },
  methods: {
    // 修正：使用 response 變量或移除它
    async checkConnection() {
      try {
        await fetch(`${BASE_URL}/health-check`, {
          method: 'HEAD',
          cache: 'no-cache'
        });
        this.networkStatus = true;
        return true;
      } catch (error) {
        this.networkStatus = false;
        return false;
      }
    },

    async retryLogin() {
      if (this.retryCount < this.maxRetries) {
        this.retryCount++;
        console.log(`Retrying login attempt ${this.retryCount} of ${this.maxRetries}`);
        await new Promise(resolve => setTimeout(resolve, 1000 * this.retryCount));
        return this.loginUser();
      }
      return false;
    },

    async loginUser() {
      if (!this.isFormValid) {
        this.loginMessage = '請輸入用戶名和密碼';
        return;
      }

      this.isLoading = true;
      this.loginMessage = '正在登錄...';

      try {
        if (!await this.checkConnection()) {
          throw new Error('NETWORK_ERROR');
        }

        const response = await fetch(`${BASE_URL}/api/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          }),
          signal: AbortSignal.timeout(10000)
        });

        console.log('Response status:', response.status);
        console.log('Response type:', response.headers.get('content-type'));

        if (response.ok) {
          const contentType = response.headers.get('content-type');
          if (!contentType || !contentType.includes('application/json')) {
            throw new Error('SERVER_ERROR');
          }

          const data = await response.json();
          this.loginSuccess = true;
          this.loginMessage = '登錄成功！';
          
          localStorage.setItem('userToken', data.token);
          localStorage.setItem('username', data.username);
          localStorage.setItem('permission', data.permission);
          localStorage.setItem('line_id', data.lineId);
          
          this.$emit('login-success', data.username);
          
          setTimeout(() => {
            window.location.reload();
          }, 500);
        } else {
          throw new Error('LOGIN_FAILED');
        }
      } catch (error) {
        console.error('Login error:', error);
        this.loginSuccess = false;

        switch(error.name) {
          case 'AbortError':
            this.loginMessage = '請求超時，請檢查網絡連接後重試';
            break;
          case 'TypeError':
            this.loginMessage = '網絡連接錯誤，請檢查網絡設置';
            if (await this.retryLogin()) return;
            break;
          default:
            switch(error.message) {
              case 'NETWORK_ERROR':
                this.loginMessage = '無法連接到服務器，請檢查網絡連接';
                break;
              case 'SERVER_ERROR':
                this.loginMessage = '服務器響應異常，請稍後重試';
                break;
              case 'LOGIN_FAILED':
                this.loginMessage = '登錄失敗，請檢查用戶名和密碼';
                break;
              default:
                this.loginMessage = '登錄過程中發生錯誤，請稍後重試';
            }
        }
      } finally {
        this.isLoading = false;
      }
    },

    resetLogin() {
      this.retryCount = 0;
      this.loginMessage = '';
      this.loginSuccess = false;
      this.isLoading = false;
    }
  },
  
  watch: {
    username() {
      this.resetLogin();
    },
    password() {
      this.resetLogin();
    }
  }
}
</script>

  <style scoped>
  .user-login {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    width: 100%;
    padding: 10px;
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
  
  .error {
    color: red;
    font-size: 0.8em;
  }
  
  .success {
    color: green;
  }
  
  .register-link {
    margin-top: 15px;
    text-align: center;
  }
  
  .register-link a {
    color: #4CAF50;
    text-decoration: none;
  }
  
  .register-link a:hover {
    text-decoration: underline;
  }
  </style>
  
  
 
  <template>
    <div class="user-register">
      <h2>用戶註冊</h2>
      <form @submit.prevent="registerUser">
        <div class="form-group">
          <label for="username">用戶名：</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required
            @input="validateUsername"
          >
          <span class="error" v-if="usernameError">{{ usernameError }}</span>
        </div>
        
        <div class="form-group">
          <label for="email">電子郵件：</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required
            @input="validateEmail"
          >
          <span class="error" v-if="emailError">{{ emailError }}</span>
        </div>
  
        <div class="form-group">
          <label for="lineId">Line ID：</label>
          <input 
            type="text" 
            id="lineId" 
            v-model="lineId" 
            required
            @input="validateLineId"
          >
          <span class="error" v-if="lineIdError">{{ lineIdError }}</span>
        </div>
        
        <div class="form-group">
          <label for="password">密碼：</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required
            @input="validatePassword"
          >
          <span class="error" v-if="passwordError">{{ passwordError }}</span>
        </div>
        
        <button type="submit" :disabled="!isFormValid">註冊</button>
      </form>
      <p v-if="registrationMessage" :class="{ 'success': registrationSuccess, 'error': !registrationSuccess }">
        {{ registrationMessage }}
      </p>
    </div>
  </template>
  
  <script>
  import { BASE_URL } from '../main';

  export default {
    name: 'UserRegister',
    data() {
      return {
        username: '',
        email: '',
        lineId: '',
        password: '',
        usernameError: '',
        emailError: '',
        lineIdError: '',
        passwordError: '',
        registrationMessage: '',
        registrationSuccess: false
      }
    },
    computed: {
      isFormValid() {
        return this.username && this.email && this.lineId && this.password &&
               !this.usernameError && !this.emailError && !this.lineIdError && !this.passwordError;
      }
    },
    
    methods: {
      validateUsername() {
        this.usernameError = this.username.length < 3 ? '用戶名至少需要3個字符' : '';
      },
      validateEmail() {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        this.emailError = !emailRegex.test(this.email) ? '請輸入有效的電子郵件地址' : '';
      },
      validateLineId() {
        this.lineIdError = this.lineId.length < 3 ? 'Line ID 至少需要3個字符' : '';
      },
      validatePassword() {
        this.passwordError = this.password.length < 6 ? '密碼至少需要6個字符' : '';
      },
      async registerUser() {
        try {
          // const response = await fetch('http://192.168.10.11:3000/register', {
          //   method: 'POST',
          //   headers: {
          //     'Content-Type': 'application/json',
              const response = await fetch(`${BASE_URL}/api/register`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
              },
            body: JSON.stringify({
              username: this.username,
              email: this.email,
              lineId: this.lineId,
              password: this.password
            }),
          });
  
          const data = await response.json();
        
          if (response.ok) {
            this.registrationSuccess = true;
            this.registrationMessage = data.message;
  
            // 清空表單字段
            this.username = '';
            this.email = '';
            this.lineId = '';
            this.password = '';
            this.usernameError = '';
            this.emailError = '';
            this.lineIdError = '';
            this.passwordError = '';
          } else {
            this.registrationSuccess = false;
            this.registrationMessage = data.message;
          }
        } catch (error) {
          console.error('Registration error:', error);
          this.registrationSuccess = false;
          this.registrationMessage = '註冊過程中發生錯誤，請稍後再試。';
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .user-register {
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
  </style>
  
   
import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from './components/MainLayout.vue';
import UserLogin from './components/UserLogin.vue';
import PhotoUpload from './components/PhotoUpload.vue'; // 上傳照片組件
import UserReview from './components/UserReview.vue'; // 審核組件
import UserStaff from './components/UserStaff.vue'; // 人員管理組件
import UserRegister from './components/UserRegister.vue';
import UserHeader from './components/UserHeader.vue';
import UserRecord from './components/UserRecord.vue';
const routes = [
  {
    path: '/',
    name: 'Main',
    component: MainLayout,
    children: [
      {
        path: 'upload',
        name: 'Upload',
        component: PhotoUpload,
      },
      {
        path: 'review',
        name: 'Review',
        component: UserReview,
      },
      {
        path: 'register',
        name: 'Register',
        component: UserRegister,
      },
      {
        path: 'staff',
        name: 'Staff',
        component: UserStaff,
      },
      {
        path: 'login',
        name: 'Login',
        component: UserLogin,
      },
      {
        path: 'header',
        name: 'Header',
        component: UserHeader,
      },
      {
        path: 'record',
        name: 'Record',
        component: UserRecord,
      }
    ],
  },
];


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;



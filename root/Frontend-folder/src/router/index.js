import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '@/views/LandingView.vue'
import HomeVeiw from '@/views/HomeVeiw.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'
import ServiceForm from '@/views/ServiceForm.vue'
import ServiceView from '@/views/ServiceView.vue'
import ServiceProForm from '@/views/ServiceProForm.vue'
import CustForm from '@/views/CustForm.vue'
import ProffesionalListView from '@/views/ProffesionalListView.vue'
import ProfileView from '@/views/ProfileView.vue'
import BookService from '@/views/BookService.vue'
import AdminDash from '@/views/AdminDash.vue'
import ServiceRequest from '@/views/ServiceRequest.vue'
import AddFeedback from '@/views/AddFeedback.vue'
import FeedbackView from '@/components/FeedbackView.vue'
import CompleteService from '@/views/CompleteService.vue'
import NotAuthView from '@/views/NotAuthView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'Home',
      component: HomeVeiw,
    },
    {
      path: '/',
      name: 'Landing',
      component: LandingView,
    },

    {
      path: '/login',
      name: 'Login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView,
    },
    {
      path: '/service/:action/:serv_id?',
      name: 'CreateService',
      component: ServiceForm,
      meta: { roles: [1] },
    },
    {
      path: '/services/:serv_id',
      name: 'Service',
      component: ServiceView,
    },
    {
      path: '/create/service_pro',
      name: 'CreateServicePro',
      component: ServiceProForm,
      meta: { roles: [2] },
    },
    {
      path: '/create/cust',
      name: 'CreateCustomer',
      component: CustForm,
      meta: { roles: [3] },
    },
    {
      path: '/professionals/:serv_id?/:serv_name?',
      name: 'AllProfessionals',
      component: ProffesionalListView,
      meta: { roles: [1, 3] },
      props: true,
    },
    {
      path: '/profile/:id?',
      name: 'Profile',
      component: ProfileView,
    },
    {
      path: '/book_service/:service_pro_id',
      name: 'BookService',
      component: BookService,
    },
    {
      path: '/dashboard',
      name: 'AdminDash',
      component: AdminDash,
      meta: { roles: [1] },
    },
    {
      path: '/requests',
      name: 'ServiceRequest',
      component: ServiceRequest,
    },
    {
      path: '/request/feedback/:rqst_id',
      name: 'AddFeedback',
      component: AddFeedback,
    },
    {
      path: '/feedbacks',
      name: 'Feedbacks',
      component: FeedbackView,
    },
    {
      path: '/requests/complete/:rqst_id',
      name: 'CompleteService',
      component: CompleteService,
    },
    {
      path: '/not-authorized',
      name: 'NotFound',
      component: NotAuthView,
    },
  ],
})

export default router

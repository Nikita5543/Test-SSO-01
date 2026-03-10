import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/auth/signin',
      name: 'SignIn',
      component: () => import('@/views/auth/SignIn.vue'),
      meta: { public: true }
    },
    {
      path: '/auth/signup',
      name: 'SignUp',
      component: () => import('@/views/auth/SignUp.vue'),
      meta: { public: true }
    },
    {
      path: '/auth/forgot-password',
      name: 'ForgotPassword',
      component: () => import('@/views/auth/ForgotPassword.vue'),
      meta: { public: true }
    },
    {
      path: '/',
      component: () => import('@/layouts/DashboardLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: () => import('@/views/dashboard/Dashboard.vue')
        },
        {
          path: 'plugins',
          name: 'Plugins',
          component: () => import('@/views/plugins/Plugins.vue')
        },
        {
          path: 'inventory',
          name: 'InventoryManager',
          component: () => import('@/views/inventory/InventoryManager.vue')
        },
        {
          path: 'performance',
          name: 'PerformanceManager',
          component: () => import('@/views/performance/PerformanceManager.vue')
        },
        {
          path: 'configuration',
          name: 'ConfigurationManager',
          component: () => import('@/views/configuration/ConfigurationManager.vue')
        },
        {
          path: 'configuration/bgp-prefix-list',
          name: 'BGPPrefixList',
          component: () => import('@/views/configuration/BGPPrefixList.vue')
        },
        {
          path: 'accounting',
          name: 'AccountingManager',
          component: () => import('@/views/accounting/AccountingManager.vue')
        },
        {
          path: 'incidents',
          name: 'IncidentManager',
          component: () => import('@/views/incidents/IncidentManager.vue')
        },
        {
          path: 'security',
          name: 'SecurityManager',
          component: () => import('@/views/security/SecurityManager.vue')
        },
        {
          path: 'users',
          name: 'Users',
          component: () => import('@/views/users/Users.vue')
        },
        {
          path: 'settings',
          name: 'Settings',
          component: () => import('@/views/settings/Settings.vue')
        },
        {
          path: 'settings/profile',
          name: 'Profile',
          component: () => import('@/views/settings/Profile.vue')
        },
        {
          path: 'settings/account',
          name: 'Account',
          component: () => import('@/views/settings/Account.vue')
        },
        {
          path: 'settings/notifications',
          name: 'Notifications',
          component: () => import('@/views/settings/Notifications.vue')
        },
        {
          path: 'settings/display',
          name: 'Display',
          component: () => import('@/views/settings/Display.vue')
        },
        {
          path: 'help',
          name: 'Help',
          component: () => import('@/views/help/Help.vue')
        },
        {
          path: '/:pathMatch(.*)*',
          name: 'NotFound',
          component: () => import('@/views/errors/NotFound.vue')
        }
      ]
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (authStore.token && !authStore.user) {
    await authStore.fetchUser()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/auth/signin')
  } else if (to.meta.public && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router

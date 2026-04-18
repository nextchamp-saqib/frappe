import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/pages/Settings.vue'),
    children: [
      { path: '', redirect: { name: 'Profile' } },
      { path: 'profile', name: 'Profile', component: () => import('@/pages/settings/Profile.vue') },
      { path: 'notifications', name: 'Notifications', component: () => import('@/pages/settings/Notifications.vue') },
      { path: 'general', name: 'General', component: () => import('@/pages/settings/General.vue') },
      { path: 'members', name: 'Members', component: () => import('@/pages/settings/Members.vue') },
      { path: 'email-account', name: 'EmailAccount', component: () => import('@/pages/settings/EmailAccount.vue') },
      { path: 'email-template', name: 'EmailTemplate', component: () => import('@/pages/settings/EmailTemplate.vue') },
      { path: 'data-import', name: 'DataImport', component: () => import('@/pages/settings/DataImport.vue') },
      { path: 'automation', name: 'Automation', component: () => import('@/pages/settings/Automation.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory('/settings'),
  routes,
})

export default router

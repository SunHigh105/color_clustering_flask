import Vue from 'vue'
import VueRouter from 'vue-router'
import Upload from '@/components/Upload'
import List from '@/components/List'

Vue.use(VueRouter)

  const routes = [
    {
      path: '/upload',
      name: 'Upload',
      component: Upload
    },
    {
      path: '/list',
      name: 'List',
      component: List
    }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

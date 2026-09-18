import { createRouter, createWebHistory } from 'vue-router'

// 안내 데스크의 층별 안내표 ─ "이 주소로 오면 이 화면을 보여준다"
const router = createRouter({
  // createWebHistory = 주소를 /links 처럼 깔끔하게 표기하는 방식 (예전: /#/links)
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: '/',
        name: 'landing',
        // () => import(...) = 손님이 해당 층에 다다르면 불이 켜지는 방식 (지연 로딩)
        // 최초 접속 시 모든 화면 코드를 한번에 받아오지 않는다 → 첫 화면 빨리 뜸
        component: () => import('@/pages/LandingPage.vue'),
    },
  ],
})

export default router

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'

// 가게(app)를 차린다 → 화이트보드(Pinia) 걸기 → 안내 데스크(Router) 배치 → 영업 시작(mount)
const app = createApp(App)

// Pinia를 Router보다 먼저 등록한다.
// 안내 데스크(Router)에서 "등록된 회원님인가"를 확인할 때 화이트보드(authStore)를 봐야 하기 때문
app.use(createPinia())
app.use(router) 

// index.html의 <div id="app"> 자리에 입주
app.mount('#app')

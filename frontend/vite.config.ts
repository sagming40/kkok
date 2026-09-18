import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// Vite = 재료(파일)를 모아 요리(화면)를 만들어 내보내는 주방장
// plugins = 주방장이 사용하는 셰프 전용 전문 도구들
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      // "@"를 사용하면 이 설정 파일 옆의 src/ 폴더를 뜻한다는 약속
      // import.meta.url = "이 파일이 지금 어디 있는지"를 알려주는 현재 위치 표지판
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})

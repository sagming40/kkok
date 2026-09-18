<script setup lang="ts">
// @/ 별칭이 동작하는지 확인 ─ src/components/ui/button을 가리킨다.
import { Button } from '@/components/ui/button'
</script>

<template>
  <!-- Tailwind 스티커 확인: 화면 꽉 채우기 + 가운데 정렬 + 간격 -->
  <main class="flex min-h-screen flex-col items-center justify-center gap-4">
    <h1 class="text-3xl font-bold">콕 눌러 줄이기</h1>
    <!-- shadcn-vue 'Button' 확인 -->
    <Button>kkok!</Button> 
  </main> 
</template>

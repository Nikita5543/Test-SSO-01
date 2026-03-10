<template>
  <div class="flex h-full flex-col items-center justify-center">
    <div class="text-center">
      <h1 class="text-6xl font-bold text-primary">404</h1>
      <p class="mt-4 text-xl text-muted-foreground">Page not found</p>
      <p class="mt-2 text-sm text-muted-foreground">
        The page you are looking for does not exist.
      </p>
      <Button class="mt-6" @click="$router.push('/dashboard')">
        Go to Dashboard
      </Button>
    </div>
  </div>
</template>

<script setup>
import Button from '@/components/ui/Button.vue'
</script>

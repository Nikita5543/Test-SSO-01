<template>
  <div class="flex min-h-screen items-center justify-center bg-background p-4">
    <Card class="w-full max-w-md">
      <CardHeader class="space-y-4 text-center">
        <div class="flex justify-center">
          <img src="/logo.png" alt="NOC Vision" class="h-16 w-16" />
        </div>
        <div>
          <CardTitle class="text-2xl font-bold">NOC Vision</CardTitle>
          <CardDescription class="mt-2">
            Network Operations Center Platform
          </CardDescription>
        </div>
      </CardHeader>
      <CardContent class="space-y-4">
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="space-y-2">
            <Label for="username">Username</Label>
            <Input
              id="username"
              v-model="form.username"
              type="text"
              placeholder="Enter your username"
              required
              :disabled="authStore.loading"
            />
          </div>
          <div class="space-y-2">
            <Label for="password">Password</Label>
            <Input
              id="password"
              v-model="form.password"
              type="password"
              placeholder="Enter your password"
              required
              :disabled="authStore.loading"
            />
          </div>
          <div class="flex items-center justify-between">
            <Checkbox
              id="remember"
              v-model="form.remember"
              label="Remember me"
            />
            <RouterLink
              to="/auth/forgot-password"
              class="text-sm text-primary hover:underline"
            >
              Forgot password?
            </RouterLink>
          </div>
          <Button
            type="submit"
            class="w-full"
            :loading="authStore.loading"
          >
            Sign In
          </Button>
        </form>

        <div v-if="authStore.error" class="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
          {{ authStore.error }}
        </div>

        <div class="text-center text-sm text-muted-foreground">
          <p>Default credentials:</p>
          <p class="font-mono text-xs">Username: admin | Password: admin</p>
        </div>
      </CardContent>
      <CardFooter class="flex justify-center">
        <p class="text-sm text-muted-foreground">
          Don't have an account?
          <RouterLink to="/auth/signup" class="text-primary hover:underline">
            Sign up
          </RouterLink>
        </p>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardFooter from '@/components/ui/CardFooter.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Checkbox from '@/components/ui/Checkbox.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: 'admin',
  password: 'admin',
  remember: false
})

async function handleSubmit() {
  const success = await authStore.login({
    username: form.username,
    password: form.password
  })

  if (success) {
    router.push('/dashboard')
  }
}
</script>

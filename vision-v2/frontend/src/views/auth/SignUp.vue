<template>
  <div class="flex min-h-screen items-center justify-center bg-background p-4">
    <Card class="w-full max-w-md">
      <CardHeader class="space-y-4 text-center">
        <div class="flex justify-center">
          <img src="/logo.png" alt="NOC Vision" class="h-16 w-16" />
        </div>
        <div>
          <CardTitle class="text-2xl font-bold">Create Account</CardTitle>
          <CardDescription class="mt-2">
            Sign up for NOC Vision platform
          </CardDescription>
        </div>
      </CardHeader>
      <CardContent class="space-y-4">
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="space-y-2">
            <Label for="fullName">Full Name</Label>
            <Input
              id="fullName"
              v-model="form.full_name"
              type="text"
              placeholder="Enter your full name"
              required
              :disabled="authStore.loading"
            />
          </div>
          <div class="space-y-2">
            <Label for="username">Username</Label>
            <Input
              id="username"
              v-model="form.username"
              type="text"
              placeholder="Choose a username"
              required
              :disabled="authStore.loading"
            />
          </div>
          <div class="space-y-2">
            <Label for="email">Email</Label>
            <Input
              id="email"
              v-model="form.email"
              type="email"
              placeholder="Enter your email"
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
              placeholder="Create a password"
              required
              :disabled="authStore.loading"
            />
          </div>
          <div class="space-y-2">
            <Label for="confirmPassword">Confirm Password</Label>
            <Input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              placeholder="Confirm your password"
              required
              :disabled="authStore.loading"
            />
          </div>
          <Button
            type="submit"
            class="w-full"
            :loading="authStore.loading"
          >
            Sign Up
          </Button>
        </form>

        <div v-if="error" class="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
          {{ error }}
        </div>
      </CardContent>
      <CardFooter class="flex justify-center">
        <p class="text-sm text-muted-foreground">
          Already have an account?
          <RouterLink to="/auth/signin" class="text-primary hover:underline">
            Sign in
          </RouterLink>
        </p>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
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

const router = useRouter()
const authStore = useAuthStore()
const error = ref('')

const form = reactive({
  full_name: '',
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

async function handleSubmit() {
  error.value = ''

  if (form.password !== form.confirmPassword) {
    error.value = 'Passwords do not match'
    return
  }

  try {
    await authStore.register({
      full_name: form.full_name,
      username: form.username,
      email: form.email,
      password: form.password
    })
    router.push('/auth/signin')
  } catch (err) {
    error.value = err.message
  }
}
</script>

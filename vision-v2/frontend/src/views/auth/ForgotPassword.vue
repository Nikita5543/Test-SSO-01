<template>
  <div class="flex min-h-screen items-center justify-center bg-background p-4">
    <Card class="w-full max-w-md">
      <CardHeader class="space-y-4 text-center">
        <div class="flex justify-center">
          <img src="/logo.png" alt="NOC Vision" class="h-16 w-16" />
        </div>
        <div>
          <CardTitle class="text-2xl font-bold">Forgot Password</CardTitle>
          <CardDescription class="mt-2">
            Enter your email to reset your password
          </CardDescription>
        </div>
      </CardHeader>
      <CardContent class="space-y-4">
        <form v-if="!submitted" @submit.prevent="handleSubmit" class="space-y-4">
          <div class="space-y-2">
            <Label for="email">Email</Label>
            <Input
              id="email"
              v-model="email"
              type="email"
              placeholder="Enter your email"
              required
            />
          </div>
          <Button type="submit" class="w-full">
            Send Reset Link
          </Button>
        </form>

        <div v-else class="rounded-md bg-primary/10 p-4 text-center">
          <p class="text-sm text-primary">
            If an account exists with this email, you will receive password reset instructions.
          </p>
        </div>
      </CardContent>
      <CardFooter class="flex justify-center">
        <RouterLink to="/auth/signin" class="text-sm text-primary hover:underline">
          Back to Sign In
        </RouterLink>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardFooter from '@/components/ui/CardFooter.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'

const email = ref('')
const submitted = ref(false)

function handleSubmit() {
  // In a real app, this would call the backend
  submitted.value = true
}
</script>

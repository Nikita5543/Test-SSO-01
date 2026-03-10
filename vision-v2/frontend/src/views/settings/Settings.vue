<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Settings</h1>
      <p class="text-muted-foreground">Manage your platform settings</p>
    </div>

    <div class="grid gap-6 md:grid-cols-2">
      <Card class="cursor-pointer hover:bg-accent/50 transition-colors" @click="$router.push('/settings/profile')">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <User class="h-5 w-5" />
            Profile
          </CardTitle>
          <CardDescription>Manage your personal information</CardDescription>
        </CardHeader>
      </Card>

      <Card class="cursor-pointer hover:bg-accent/50 transition-colors" @click="$router.push('/settings/account')">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Settings class="h-5 w-5" />
            Account
          </CardTitle>
          <CardDescription>Manage your account settings</CardDescription>
        </CardHeader>
      </Card>

      <Card class="cursor-pointer hover:bg-accent/50 transition-colors" @click="$router.push('/settings/notifications')">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Bell class="h-5 w-5" />
            Notifications
          </CardTitle>
          <CardDescription>Configure notification preferences</CardDescription>
        </CardHeader>
      </Card>

      <Card class="cursor-pointer hover:bg-accent/50 transition-colors" @click="$router.push('/settings/display')">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Monitor class="h-5 w-5" />
            Display
          </CardTitle>
          <CardDescription>Customize your display preferences</CardDescription>
        </CardHeader>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { User, Settings, Bell, Monitor } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
</script>

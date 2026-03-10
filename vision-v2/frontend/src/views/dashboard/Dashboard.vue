<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Dashboard</h1>
      <p class="text-muted-foreground">Welcome to NOC Vision - Network Operations Center Platform</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card v-for="stat in stats" :key="stat.title">
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">{{ stat.title }}</CardTitle>
          <component :is="stat.icon" class="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ stat.value }}</div>
          <p class="text-xs text-muted-foreground">{{ stat.description }}</p>
        </CardContent>
      </Card>
    </div>

    <!-- Content Placeholder -->
    <Card>
      <CardHeader>
        <CardTitle>Overview</CardTitle>
        <CardDescription>
          Dashboard content will be implemented here
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="h-[300px] flex items-center justify-center border-2 border-dashed border-muted rounded-lg">
          <p class="text-muted-foreground">Dashboard widgets coming soon</p>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { Server, AlertTriangle, Users, Activity } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'

const stats = [
  {
    title: 'Total Devices',
    value: '0',
    description: 'Network devices monitored',
    icon: Server
  },
  {
    title: 'Active Alerts',
    value: '0',
    description: 'Incidents requiring attention',
    icon: AlertTriangle
  },
  {
    title: 'Users',
    value: '1',
    description: 'Registered platform users',
    icon: Users
  },
  {
    title: 'Uptime',
    value: '99.9%',
    description: 'Network availability',
    icon: Activity
  }
]
</script>

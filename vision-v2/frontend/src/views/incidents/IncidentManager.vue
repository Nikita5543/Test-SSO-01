<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Incident Manager</h1>
      <p class="text-muted-foreground">Track and manage network incidents</p>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>Incident Tracking</CardTitle>
        <CardDescription>
          Incident content will be implemented here
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="h-[400px] flex items-center justify-center border-2 border-dashed border-muted rounded-lg">
          <p class="text-muted-foreground">Incident manager coming soon</p>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Security Manager</h1>
      <p class="text-muted-foreground">Manage network security policies</p>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>Security Policies</CardTitle>
        <CardDescription>
          Security content will be implemented here
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="h-[400px] flex items-center justify-center border-2 border-dashed border-muted rounded-lg">
          <p class="text-muted-foreground">Security manager coming soon</p>
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

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Configuration Manager</h1>
      <p class="text-muted-foreground">Manage network device configurations</p>
    </div>

    <!-- Configuration Tools Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- BGP Prefix-list Card -->
      <Card class="cursor-pointer hover:border-primary transition-colors" @click="$router.push('/configuration/bgp-prefix-list')">
        <CardHeader>
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>
              <path d="M2 12h20"/>
            </svg>
            <CardTitle>BGP Prefix-list</CardTitle>
          </div>
          <CardDescription>
            Update BGP prefix-lists on Juniper MX devices using bgpq4
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-muted-foreground">
            Generate and apply prefix-lists from ASN data via NETCONF
          </p>
        </CardContent>
      </Card>

      <!-- Placeholder for future tools -->
      <Card class="opacity-50">
        <CardHeader>
          <CardTitle>More Tools</CardTitle>
          <CardDescription>
            Additional configuration tools coming soon
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-muted-foreground">
            Stay tuned for more configuration management features
          </p>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup>
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
</script>

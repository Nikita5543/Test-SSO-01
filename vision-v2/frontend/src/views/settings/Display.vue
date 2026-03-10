<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Display</h1>
      <p class="text-muted-foreground">Customize your display preferences</p>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>Display Settings</CardTitle>
        <CardDescription>
          Choose your preferred theme
        </CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium">Theme</p>
            <p class="text-sm text-muted-foreground">Select your preferred color scheme</p>
          </div>
          <div class="flex gap-2">
            <Button
              v-for="option in themeOptions"
              :key="option.value"
              :variant="themeStore.theme === option.value ? 'default' : 'outline'"
              size="sm"
              @click="themeStore.setTheme(option.value)"
            >
              <component :is="option.icon" class="mr-2 h-4 w-4" />
              {{ option.label }}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { Sun, Moon, Monitor } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'

const themeStore = useThemeStore()

const themeOptions = [
  { value: 'light', label: 'Light', icon: Sun },
  { value: 'dark', label: 'Dark', icon: Moon },
  { value: 'system', label: 'System', icon: Monitor }
]
</script>

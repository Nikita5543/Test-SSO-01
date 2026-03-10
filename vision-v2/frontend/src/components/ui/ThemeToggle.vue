<template>
  <DropdownMenu align="end">
    <template #trigger>
      <Button variant="ghost" size="icon">
        <Sun v-if="themeStore.effectiveTheme === 'light'" class="h-5 w-5" />
        <Moon v-else-if="themeStore.effectiveTheme === 'dark'" class="h-5 w-5" />
        <Monitor v-else class="h-5 w-5" />
        <span class="sr-only">Toggle theme</span>
      </Button>
    </template>

    <DropdownMenuItem
      v-for="option in themeOptions"
      :key="option.value"
      :class="themeStore.theme === option.value && 'bg-accent'"
      @select="themeStore.setTheme(option.value)"
    >
      <component :is="option.icon" class="mr-2 h-4 w-4" />
      {{ option.label }}
    </DropdownMenuItem>
  </DropdownMenu>
</template>

<script setup>
import { Sun, Moon, Monitor } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme'
import Button from './Button.vue'
import DropdownMenu from './DropdownMenu.vue'
import DropdownMenuItem from './DropdownMenuItem.vue'

const themeStore = useThemeStore()

const themeOptions = [
  { value: 'light', label: 'Light', icon: Sun },
  { value: 'dark', label: 'Dark', icon: Moon },
  { value: 'system', label: 'System', icon: Monitor }
]
</script>

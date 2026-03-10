<template>
  <RouterLink
    :to="item.path"
    :class="cn(
      'flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground',
      isActive && 'bg-accent text-accent-foreground',
      isSubItem && 'text-muted-foreground'
    )"
  >
    <component :is="item.icon" class="h-4 w-4" />
    {{ item.label }}
  </RouterLink>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { cn } from '@/lib/utils'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  isSubItem: {
    type: Boolean,
    default: false
  }
})

const route = useRoute()

const isActive = computed(() => route.path === props.item.path)
</script>

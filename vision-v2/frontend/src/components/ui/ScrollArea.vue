<template>
  <div :class="cn('relative overflow-hidden', props.class)">
    <div
      ref="viewportRef"
      class="h-full w-full overflow-auto scrollbar-thin scrollbar-thumb-muted scrollbar-track-transparent"
      @scroll="handleScroll"
    >
      <slot />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['scroll'])
const viewportRef = ref(null)

function handleScroll(event) {
  emit('scroll', event)
}

function scrollTo(options) {
  viewportRef.value?.scrollTo(options)
}

function scrollTop() {
  viewportRef.value?.scrollTo({ top: 0, behavior: 'smooth' })
}

defineExpose({ scrollTo, scrollTop, viewportRef })
</script>

<style scoped>
.scrollbar-thin::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: hsl(var(--muted));
  border-radius: 3px;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background-color: hsl(var(--muted-foreground) / 0.3);
}
</style>

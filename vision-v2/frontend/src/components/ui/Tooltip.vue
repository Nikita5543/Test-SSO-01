<template>
  <div class="relative inline-block" @mouseenter="show" @mouseleave="hide">
    <slot />
    <Transition
      enter-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isVisible"
        :class="cn(
          'absolute z-50 px-2 py-1 text-xs text-primary-foreground bg-primary rounded shadow-sm whitespace-nowrap pointer-events-none',
          position === 'top' && 'bottom-full left-1/2 -translate-x-1/2 mb-1',
          position === 'bottom' && 'top-full left-1/2 -translate-x-1/2 mt-1',
          position === 'left' && 'right-full top-1/2 -translate-y-1/2 mr-1',
          position === 'right' && 'left-full top-1/2 -translate-y-1/2 ml-1',
          props.class
        )"
      >
        {{ content }}
        <div
          :class="cn(
            'absolute w-1.5 h-1.5 bg-primary rotate-45',
            position === 'top' && 'top-full left-1/2 -translate-x-1/2 -mt-0.5',
            position === 'bottom' && 'bottom-full left-1/2 -translate-x-1/2 -mb-0.5',
            position === 'left' && 'left-full top-1/2 -translate-y-1/2 -ml-0.5',
            position === 'right' && 'right-full top-1/2 -translate-y-1/2 -mr-0.5'
          )"
        />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  position: {
    type: String,
    default: 'top',
    validator: (value) => ['top', 'bottom', 'left', 'right'].includes(value)
  },
  class: {
    type: String,
    default: ''
  }
})

const isVisible = ref(false)

function show() {
  isVisible.value = true
}

function hide() {
  isVisible.value = false
}
</script>

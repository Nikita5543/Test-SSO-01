<template>
  <button
    :class="cn(
      'relative flex w-full cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground hover:bg-accent hover:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
      inset && 'pl-8',
      props.class
    )"
    @click="handleClick"
  >
    <slot />
  </button>
</template>

<script setup>
import { cn } from '@/lib/utils'

const props = defineProps({
  inset: {
    type: Boolean,
    default: false
  },
  class: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['select'])

function handleClick() {
  emit('select')
}
</script>

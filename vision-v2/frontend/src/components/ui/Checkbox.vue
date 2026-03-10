<template>
  <div class="flex items-center space-x-2">
    <input
      type="checkbox"
      :id="id"
      :checked="modelValue"
      @change="$emit('update:modelValue', $event.target.checked)"
      :class="cn(
        'peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground',
        props.class
      )"
    />
    <Label v-if="label" :for="id" class="text-sm font-normal cursor-pointer">
      {{ label }}
    </Label>
  </div>
</template>

<script setup>
import { cn } from '@/lib/utils'
import Label from './Label.vue'

defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  id: {
    type: String,
    required: true
  },
  label: {
    type: String,
    default: ''
  },
  class: {
    type: String,
    default: ''
  }
})

defineEmits(['update:modelValue'])
</script>

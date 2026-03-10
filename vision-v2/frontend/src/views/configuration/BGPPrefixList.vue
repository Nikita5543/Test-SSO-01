<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">BGP Prefix-list Manager</h1>
      <p class="text-muted-foreground">
        Update BGP prefix-lists on Juniper MX devices using bgpq4
      </p>
    </div>

    <!-- Configuration Form -->
    <Card>
      <CardHeader>
        <CardTitle>Update Prefix-list</CardTitle>
        <CardDescription>
          Generate and apply prefix-lists from ASN using bgpq4 utility
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Device Selection -->
          <div class="space-y-2">
            <Label for="device">Device</Label>
            <select
              id="device"
              v-model="form.device_id"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              required
              :disabled="loading || devices.length === 0"
            >
              <option value="" disabled>Select a device</option>
              <option v-for="device in devices" :key="device.id" :value="device.id">
                {{ device.name }} ({{ device.hostname }})
              </option>
            </select>
            <p v-if="devices.length === 0" class="text-sm text-muted-foreground">
              No devices available
            </p>
          </div>

          <!-- ASN Input -->
          <div class="space-y-2">
            <Label for="asn">Autonomous System Number (ASN)</Label>
            <Input
              id="asn"
              v-model="form.asn"
              placeholder="e.g., AS15169 or 15169"
              required
              :disabled="loading"
            />
            <p class="text-sm text-muted-foreground">
              Enter the ASN to generate prefix-list from (e.g., AS15169 for Google)
            </p>
          </div>

          <!-- Prefix-list Name -->
          <div class="space-y-2">
            <Label for="prefix-list-name">Prefix-list Name</Label>
            <Input
              id="prefix-list-name"
              v-model="form.prefix_list_name"
              placeholder="e.g., GOOGLE-PREFIXES"
              required
              :disabled="loading"
            />
          </div>

          <!-- Protocol Selection -->
          <div class="space-y-2">
            <Label for="protocol">Protocol</Label>
            <select
              id="protocol"
              v-model="form.protocol"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              :disabled="loading"
            >
              <option value="ipv4">IPv4</option>
              <option value="ipv6">IPv6</option>
            </select>
          </div>

          <!-- Max Prefixes -->
          <div class="space-y-2">
            <Label for="max-prefixes">Max Prefixes (Optional)</Label>
            <Input
              id="max-prefixes"
              v-model="form.max_prefixes"
              type="number"
              placeholder="e.g., 1000"
              :disabled="loading"
            />
            <p class="text-sm text-muted-foreground">
              Limit the number of prefixes generated (leave empty for no limit)
            </p>
          </div>

          <!-- Submit Button -->
          <div class="flex items-center gap-4 pt-4">
            <Button type="submit" :disabled="loading || !isFormValid">
              <span v-if="loading" class="mr-2">
                <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </span>
              {{ loading ? 'Updating...' : 'Update Prefix-list' }}
            </Button>
            <Button type="button" variant="outline" @click="resetForm" :disabled="loading">
              Reset
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>

    <!-- Result Card -->
    <Card v-if="result" :class="result.success ? 'border-green-500' : 'border-red-500'">
      <CardHeader>
        <CardTitle :class="result.success ? 'text-green-600' : 'text-red-600'">
          {{ result.success ? 'Success' : 'Error' }}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div class="space-y-2">
          <p><strong>Device:</strong> {{ result.device }}</p>
          <p><strong>Prefix-list:</strong> {{ result.prefix_list }}</p>
          <p><strong>ASN:</strong> {{ result.asn }}</p>
          <p><strong>Prefixes Generated:</strong> {{ result.prefixes_generated }}</p>
          <p><strong>Prefixes Applied:</strong> {{ result.prefixes_applied }}</p>
          <p><strong>Message:</strong> {{ result.message }}</p>
          
          <!-- Generated Prefixes -->
          <div v-if="result.details?.generated_prefixes?.length > 0" class="mt-4">
            <h4 class="font-semibold mb-2">Generated Prefixes:</h4>
            <ScrollArea class="h-[200px] w-full rounded-md border p-4">
              <ul class="space-y-1">
                <li v-for="(prefix, index) in result.details.generated_prefixes" :key="index" class="text-sm font-mono">
                  {{ prefix }}
                </li>
              </ul>
            </ScrollArea>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Available Devices Info -->
    <Card>
      <CardHeader>
        <CardTitle>Available Devices</CardTitle>
        <CardDescription>
          Juniper MX devices configured for BGP prefix-list updates
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div v-if="devices.length === 0" class="text-muted-foreground">
          No devices configured. Please add devices to the system.
        </div>
        <div v-else class="space-y-2">
          <div
            v-for="device in devices"
            :key="device.id"
            class="flex items-center justify-between p-3 rounded-lg border"
          >
            <div>
              <p class="font-medium">{{ device.name }}</p>
              <p class="text-sm text-muted-foreground">{{ device.hostname }}:{{ device.port }}</p>
            </div>
            <Badge variant="outline">{{ device.id }}</Badge>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Information Card -->
    <Card>
      <CardHeader>
        <CardTitle>About bgpq4</CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-sm text-muted-foreground">
          This tool uses <a href="https://github.com/bgp/bgpq4" target="_blank" class="text-primary hover:underline">bgpq4</a> 
          to generate prefix-lists from BGP data. bgpq4 is a utility that generates prefix-lists 
          (and config snippets) for various routing platforms based on routing databases 
          (RIPE, APNIC, etc.).
        </p>
        <div class="mt-4 space-y-2">
          <h4 class="font-semibold">How it works:</h4>
          <ol class="list-decimal list-inside text-sm text-muted-foreground space-y-1">
            <li>Enter the ASN you want to generate prefixes for</li>
            <li>Specify a name for the prefix-list</li>
            <li>Select the target Juniper MX device</li>
            <li>The system uses bgpq4 to query routing databases and generate the prefix-list</li>
            <li>The prefix-list is applied to the device via NETCONF protocol</li>
          </ol>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Badge from '@/components/ui/Badge.vue'
import ScrollArea from '@/components/ui/ScrollArea.vue'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Reactive state
const devices = ref([])
const loading = ref(false)
const result = ref(null)
const form = ref({
  device_id: '',
  asn: '',
  prefix_list_name: '',
  protocol: 'ipv4',
  max_prefixes: ''
})

// Computed
const isFormValid = computed(() => {
  return form.value.device_id && 
         form.value.asn && 
         form.value.prefix_list_name
})

// Methods
const fetchDevices = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`${API_URL}/api/v1/bgp/devices`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch devices')
    }
    
    const data = await response.json()
    devices.value = data.devices || []
  } catch (error) {
    console.error('Error fetching devices:', error)
    // Use empty array on error
    devices.value = []
  }
}

const handleSubmit = async () => {
  if (!isFormValid.value) return
  
  loading.value = true
  result.value = null
  
  try {
    const token = localStorage.getItem('token')
    const payload = {
      device_id: form.value.device_id,
      asn: form.value.asn,
      prefix_list_name: form.value.prefix_list_name,
      protocol: form.value.protocol,
      max_prefixes: form.value.max_prefixes ? parseInt(form.value.max_prefixes) : null
    }
    
    const response = await fetch(`${API_URL}/api/v1/bgp/update-prefix-list`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.detail || 'Failed to update prefix-list')
    }
    
    result.value = data
  } catch (error) {
    result.value = {
      success: false,
      device: form.value.device_id,
      prefix_list: form.value.prefix_list_name,
      asn: form.value.asn,
      prefixes_generated: 0,
      prefixes_applied: 0,
      message: error.message,
      details: {}
    }
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  form.value = {
    device_id: '',
    asn: '',
    prefix_list_name: '',
    protocol: 'ipv4',
    max_prefixes: ''
  }
  result.value = null
}

// Lifecycle
onMounted(() => {
  fetchDevices()
})
</script>

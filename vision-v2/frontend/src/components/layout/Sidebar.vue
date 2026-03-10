<template>
  <div class="flex h-full flex-col">
    <!-- Logo -->
    <div class="flex h-16 items-center border-b px-6">
      <RouterLink to="/dashboard" class="flex items-center gap-3">
        <img src="/logo.png" alt="NOC Vision" class="h-8 w-8" />
        <span class="text-lg font-bold">NOC Vision</span>
      </RouterLink>
      <Button
        variant="ghost"
        size="icon"
        class="ml-auto lg:hidden"
        @click="$emit('close')"
      >
        <X class="h-5 w-5" />
      </Button>
    </div>

    <!-- Navigation -->
    <ScrollArea class="flex-1 py-4">
      <nav class="space-y-1 px-3">
        <!-- General Section -->
        <div class="mb-4">
          <h4 class="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            General
          </h4>
          <SidebarItem
            v-for="item in generalItems"
            :key="item.path"
            :item="item"
          />
        </div>

        <!-- Pages Section -->
        <div class="mb-4">
          <h4 class="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Pages
          </h4>
          <Collapsible default-open>
            <template #trigger="{ isOpen }">
              <button
                :class="cn(
                  'flex w-full items-center justify-between rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground',
                  isAuthActive && 'bg-accent text-accent-foreground'
                )"
              >
                <div class="flex items-center gap-3">
                  <Shield class="h-4 w-4" />
                  Auth
                </div>
                <ChevronDown
                  :class="cn('h-4 w-4 transition-transform', isOpen && 'rotate-180')"
                />
              </button>
            </template>
            <div class="ml-4 mt-1 space-y-1 border-l pl-3">
              <SidebarItem
                v-for="item in authItems"
                :key="item.path"
                :item="item"
                is-sub-item
              />
            </div>
          </Collapsible>
          <SidebarItem
            v-for="item in pageItems"
            :key="item.path"
            :item="item"
          />
        </div>

        <!-- Other Section -->
        <div class="mb-4">
          <h4 class="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Other
          </h4>
          <Collapsible default-open>
            <template #trigger="{ isOpen }">
              <button
                :class="cn(
                  'flex w-full items-center justify-between rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground',
                  isSettingsActive && 'bg-accent text-accent-foreground'
                )"
              >
                <div class="flex items-center gap-3">
                  <Settings class="h-4 w-4" />
                  Settings
                </div>
                <ChevronDown
                  :class="cn('h-4 w-4 transition-transform', isOpen && 'rotate-180')"
                />
              </button>
            </template>
            <div class="ml-4 mt-1 space-y-1 border-l pl-3">
              <SidebarItem
                v-for="item in settingsItems"
                :key="item.path"
                :item="item"
                is-sub-item
              />
            </div>
          </Collapsible>
          <SidebarItem
            v-for="item in otherItems"
            :key="item.path"
            :item="item"
          />
        </div>
      </nav>
    </ScrollArea>

    <!-- Footer -->
    <div class="border-t p-4">
      <div class="flex items-center gap-3 rounded-md bg-muted p-3">
        <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-bold">
          NV
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium truncate">NOC Vision</p>
          <p class="text-xs text-muted-foreground truncate">v1.0.0</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  LayoutDashboard,
  Puzzle,
  Package,
  BarChart3,
  Settings2,
  Calculator,
  AlertTriangle,
  Shield,
  Users,
  User,
  Settings,
  Bell,
  Monitor,
  HelpCircle,
  X,
  ChevronDown,
  LogIn,
  UserPlus,
  KeyRound
} from 'lucide-vue-next'
import { cn } from '@/lib/utils'
import Button from '@/components/ui/Button.vue'
import ScrollArea from '@/components/ui/ScrollArea.vue'
import Collapsible from '@/components/ui/Collapsible.vue'
import SidebarItem from './SidebarItem.vue'

const route = useRoute()

defineEmits(['close'])

const generalItems = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/plugins', label: 'Plugins', icon: Puzzle },
  { path: '/inventory', label: 'Inventory Manager', icon: Package },
  { path: '/performance', label: 'Performance Manager', icon: BarChart3 },
  { path: '/configuration', label: 'Configuration Manager', icon: Settings2 },
  { path: '/accounting', label: 'Accounting Manager', icon: Calculator },
  { path: '/incidents', label: 'Incident Manager', icon: AlertTriangle },
  { path: '/security', label: 'Security Manager', icon: Shield }
]

const authItems = [
  { path: '/auth/signin', label: 'Sign In', icon: LogIn },
  { path: '/auth/signup', label: 'Sign Up', icon: UserPlus },
  { path: '/auth/forgot-password', label: 'Forgot Password', icon: KeyRound }
]

const pageItems = [
  { path: '/users', label: 'Users', icon: Users }
]

const settingsItems = [
  { path: '/settings/profile', label: 'Profile', icon: User },
  { path: '/settings/account', label: 'Account', icon: Settings },
  { path: '/settings/notifications', label: 'Notifications', icon: Bell },
  { path: '/settings/display', label: 'Display', icon: Monitor }
]

const otherItems = [
  { path: '/help', label: 'Help', icon: HelpCircle }
]

const isAuthActive = computed(() => {
  return authItems.some(item => route.path === item.path)
})

const isSettingsActive = computed(() => {
  return settingsItems.some(item => route.path === item.path)
})
</script>

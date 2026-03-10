<template>
  <div class="flex h-screen overflow-hidden bg-background">
    <!-- Sidebar -->
    <aside
      :class="cn(
        'fixed inset-y-0 left-0 z-50 flex w-72 flex-col border-r bg-card transition-transform duration-300 lg:static lg:translate-x-0',
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      )"
    >
      <Sidebar @close="isSidebarOpen = false" />
    </aside>

    <!-- Mobile Sidebar Overlay -->
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 z-40 bg-black/50 lg:hidden"
      @click="isSidebarOpen = false"
    />

    <!-- Main Content -->
    <div class="flex flex-1 flex-col overflow-hidden">
      <!-- Header -->
      <header class="flex h-16 items-center justify-between border-b bg-card px-4 lg:px-8">
        <div class="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            class="lg:hidden"
            @click="isSidebarOpen = true"
          >
            <Menu class="h-5 w-5" />
          </Button>
          <h1 class="text-lg font-semibold lg:hidden">NOC Vision</h1>
        </div>

        <div class="flex items-center gap-2">
          <ThemeToggle />
          
          <DropdownMenu align="end">
            <template #trigger>
              <Button variant="ghost" size="icon" class="relative">
                <Bell class="h-5 w-5" />
                <span class="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-destructive" />
              </Button>
            </template>
            <div class="p-4 text-sm text-muted-foreground">
              No new notifications
            </div>
          </DropdownMenu>

          <DropdownMenu align="end">
            <template #trigger>
              <Button variant="ghost" class="relative h-8 w-8 rounded-full">
                <Avatar
                  :fallback="userInitials"
                  class="h-8 w-8"
                />
              </Button>
            </template>
            <div class="px-2 py-1.5">
              <p class="text-sm font-medium">{{ authStore.user?.full_name || authStore.user?.username }}</p>
              <p class="text-xs text-muted-foreground">{{ authStore.user?.email }}</p>
            </div>
            <DropdownMenuSeparator />
            <DropdownMenuItem @select="$router.push('/settings/profile')">
              <User class="mr-2 h-4 w-4" />
              Profile
            </DropdownMenuItem>
            <DropdownMenuItem @select="$router.push('/settings')">
              <Settings class="mr-2 h-4 w-4" />
              Settings
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem @select="handleLogout">
              <LogOut class="mr-2 h-4 w-4" />
              Log out
            </DropdownMenuItem>
          </DropdownMenu>
        </div>
      </header>

      <!-- Page Content -->
      <main class="flex-1 overflow-auto p-4 lg:p-8">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Menu, Bell, User, Settings, LogOut } from 'lucide-vue-next'
import { cn } from '@/lib/utils'
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/layout/Sidebar.vue'
import Button from '@/components/ui/Button.vue'
import Avatar from '@/components/ui/Avatar.vue'
import DropdownMenu from '@/components/ui/DropdownMenu.vue'
import DropdownMenuItem from '@/components/ui/DropdownMenuItem.vue'
import DropdownMenuSeparator from '@/components/ui/DropdownMenuSeparator.vue'
import ThemeToggle from '@/components/ui/ThemeToggle.vue'

const router = useRouter()
const authStore = useAuthStore()
const isSidebarOpen = ref(false)

const userInitials = computed(() => {
  const name = authStore.user?.full_name || authStore.user?.username || ''
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

function handleLogout() {
  authStore.logout()
  router.push('/auth/signin')
}
</script>

<script setup lang="ts">
import { Sidebar } from 'frappe-ui'
import { computed } from 'vue'
import { RouterView, useRoute, useRouter } from 'vue-router'
import SettingsIcon from '~icons/lucide/settings'
import ChevronLeft from '~icons/lucide/chevron-left'
import Users from '~icons/lucide/users'
import Mail from '~icons/lucide/mail'
import FileText from '~icons/lucide/file-text'
import Database from '~icons/lucide/database'
import Zap from '~icons/lucide/zap'
import UserCircle from '~icons/lucide/user-circle'
import Bell from '~icons/lucide/bell'

const route = useRoute()
const router = useRouter()

const userNavItems = [
	{ name: 'Profile', path: 'profile', label: 'Profile', icon: UserCircle },
	{ name: 'Notifications', path: 'notifications', label: 'Notifications', icon: Bell },
]

const appNavItems = [
	{ name: 'General', path: 'general', label: 'General', icon: SettingsIcon },
	{ name: 'Members', path: 'members', label: 'Members', icon: Users },
	{ name: 'EmailAccount', path: 'email-account', label: 'Email account', icon: Mail },
	{ name: 'EmailTemplate', path: 'email-template', label: 'Email template', icon: FileText },
	{ name: 'DataImport', path: 'data-import', label: 'Data import', icon: Database },
	{ name: 'Automation', path: 'automation', label: 'Automation', icon: Zap },
]

const sidebarSections = computed(() => [
	{
		label: 'User settings',
		items: userNavItems.map((item) => ({
			label: item.label,
			icon: item.icon,
			isActive: route.name === item.name,
			onClick: () => router.push({ name: item.name }),
		})),
	},
	{
		label: 'App settings',
		items: appNavItems.map((item) => ({
			label: item.label,
			icon: item.icon,
			isActive: route.name === item.name,
			onClick: () => router.push({ name: item.name }),
		})),
	},
])
</script>

<template>
	<div class="flex h-screen bg-surface-gray-1">
		<div class="flex flex-col">
			<div class="">
				<div class="flex h-10 items-center border-b border-r px-4">
					<ChevronLeft class="mr-2 h-4 w-4 text-ink-gray-7" />
					<span class="text-sm font-medium">Settings</span>
				</div>
			</div>
			<Sidebar :sections="sidebarSections" :disable-collapse="true" />
		</div>
		<main class="flex-1 overflow-y-auto bg-surface-white">
			<RouterView />
		</main>
	</div>
</template>

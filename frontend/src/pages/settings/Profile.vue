<script setup lang="ts">
import { Button, FormControl } from 'frappe-ui'
import { ref } from 'vue'
import MonitorIcon from '~icons/lucide/monitor'
import LogOutIcon from '~icons/lucide/log-out'
import AlertTriangleIcon from '~icons/lucide/alert-triangle'
import ChevronRightIcon from '~icons/lucide/chevron-right'

const username = ref('Jayaprakash')
const avatarUrl = ref('')
const enable2FA = ref(true)
const selectedTheme = ref<'light' | 'dark' | 'system'>('light')

const userEmail = 'jayaprakash@timeless.co'

const devices = ref([
	{
		id: 1,
		browser: 'Chrome on mac OS Sequoia',
		os: 'macOS 15.0',
		location: 'Chennai, India',
		isCurrent: true,
	},
	{
		id: 2,
		browser: 'Safari on mac OS Sequoia',
		os: '',
		location: 'Mumbai, India',
		isCurrent: false,
	},
])

function triggerAvatarUpload() {
	document.getElementById('avatar-input')?.click()
}

function onAvatarChange(e: Event) {
	const file = (e.target as HTMLInputElement).files?.[0]
	if (file) {
		avatarUrl.value = URL.createObjectURL(file)
	}
}

function removeAvatar() {
	avatarUrl.value = ''
}

function signOutDevice(id: number) {
	devices.value = devices.value.filter((d) => d.id !== id)
}

function signOutAll() {
	devices.value = []
}

function getInitials(name: string) {
	return name
		.split(' ')
		.map((n) => n[0])
		.join('')
		.toUpperCase()
		.slice(0, 2)
}
</script>

<template>
	<div class="mx-auto max-w-2xl px-10 py-8">
		<h1 class="mb-6 text-xl font-semibold text-ink-gray-9">Profile</h1>

		<!-- Avatar row -->
		<div class="mb-6 flex items-center gap-5">
			<!-- Avatar -->
			<div
				class="relative flex h-16 w-16 flex-shrink-0 items-center justify-center overflow-hidden rounded-full bg-surface-gray-3 text-ink-gray-6 text-lg font-semibold select-none"
			>
				<img
					v-if="avatarUrl"
					:src="avatarUrl"
					alt="Avatar"
					class="h-full w-full object-cover"
				/>
				<span v-else>{{ getInitials(username) }}</span>
			</div>
			<div class="flex flex-col gap-1.5">
				<p class="text-sm font-medium text-ink-gray-8">{{ username }}</p>
				<p class="text-xs text-ink-gray-5">{{ userEmail }}</p>
				<div class="flex gap-2 mt-0.5">
					<Button variant="outline" size="sm" @click="removeAvatar">Remove</Button>
					<Button variant="outline" size="sm" @click="triggerAvatarUpload">
						Upload image
					</Button>
					<input
						id="avatar-input"
						type="file"
						accept="image/*"
						class="hidden"
						@change="onAvatarChange"
					/>
				</div>
			</div>
		</div>

		<!-- User name -->
		<div class="mb-8">
			<FormControl
				label="User name"
				v-model="username"
				type="text"
				placeholder="Enter user name"
			/>
		</div>

		<hr class="mb-8 border-outline-gray-2" />

		<!-- Account info & security -->
		<section class="mb-8">
			<h2 class="mb-4 text-base font-semibold text-ink-gray-9">
				Account info &amp; security
			</h2>

			<!-- Email -->
			<div class="flex items-center justify-between border-b border-outline-gray-1 py-4">
				<div>
					<p class="text-sm font-medium text-ink-gray-9">Email</p>
					<p class="text-xs text-ink-gray-5 mt-0.5">{{ userEmail }}</p>
				</div>
				<Button variant="outline" size="sm">Change email</Button>
			</div>

			<!-- Password -->
			<div class="flex items-center justify-between border-b border-outline-gray-1 py-4">
				<div>
					<p class="text-sm font-medium text-ink-gray-9">Password</p>
					<p class="text-xs text-ink-gray-5 mt-0.5">
						Changing your account password for security.
					</p>
				</div>
				<Button variant="outline" size="sm">Change password</Button>
			</div>

			<!-- 2FA -->
			<div class="flex items-center justify-between py-4">
				<div>
					<p class="text-sm font-medium text-ink-gray-9">2FA Authentication</p>
					<p class="text-xs text-ink-gray-5 mt-0.5">
						Manage two-factor authentication and security methods.
					</p>
				</div>
				<FormControl type="checkbox" v-model="enable2FA" />
			</div>
		</section>

		<hr class="mb-8 border-outline-gray-2" />

		<!-- Appearance -->
		<section class="mb-8">
			<h2 class="mb-4 text-base font-semibold text-ink-gray-9">Appearance</h2>

			<div>
				<p class="mb-3 text-sm font-medium text-ink-gray-8">Theme</p>
				<p class="mb-4 text-xs text-ink-gray-5">
					Switch between light, dark, or system theme.
				</p>
				<div class="flex gap-3">
					<!-- Light -->
					<button
						class="flex flex-col items-start gap-1.5 cursor-pointer group"
						@click="selectedTheme = 'light'"
					>
						<div
							:class="[
								'w-40 rounded-lg border-2 overflow-hidden transition-colors',
								selectedTheme === 'light'
									? 'border-blue-500'
									: 'border-outline-gray-2 group-hover:border-outline-gray-3',
							]"
						>
							<!-- Mock browser chrome -->
							<div class="bg-gray-100 px-2 py-1.5 flex gap-1">
								<span class="h-2 w-2 rounded-full bg-red-400"></span>
								<span class="h-2 w-2 rounded-full bg-yellow-400"></span>
								<span class="h-2 w-2 rounded-full bg-green-400"></span>
							</div>
							<!-- Mock content -->
							<div class="bg-white px-2 py-2 flex gap-1.5">
								<div class="w-8 shrink-0 flex flex-col gap-1">
									<div class="flex items-center gap-1 mb-1">
										<div class="h-3 w-3 rounded bg-purple-500"></div>
									</div>
									<div class="h-1.5 w-full rounded bg-gray-100"></div>
									<div class="h-1.5 w-full rounded bg-gray-100"></div>
								</div>
								<div class="flex-1 flex flex-col gap-1">
									<div class="h-1.5 w-full rounded bg-gray-200"></div>
									<div class="h-1.5 w-3/4 rounded bg-gray-100"></div>
								</div>
							</div>
						</div>
						<div class="flex items-center gap-1.5 w-full px-0.5">
							<span class="text-xs text-ink-gray-7 font-medium flex-1 text-left"
								>Light</span
							>
							<div
								:class="[
									'h-3.5 w-3.5 rounded-full border-2 flex items-center justify-center transition-colors',
									selectedTheme === 'light'
										? 'border-blue-500 bg-blue-500'
										: 'border-outline-gray-3 bg-white',
								]"
							>
								<div
									v-if="selectedTheme === 'light'"
									class="h-1.5 w-1.5 rounded-full bg-white"
								></div>
							</div>
						</div>
					</button>

					<!-- Dark -->
					<button
						class="flex flex-col items-start gap-1.5 cursor-pointer group"
						@click="selectedTheme = 'dark'"
					>
						<div
							:class="[
								'w-40 rounded-lg border-2 overflow-hidden transition-colors',
								selectedTheme === 'dark'
									? 'border-blue-500'
									: 'border-outline-gray-2 group-hover:border-outline-gray-3',
							]"
						>
							<div class="bg-gray-800 px-2 py-1.5 flex gap-1">
								<span class="h-2 w-2 rounded-full bg-red-400"></span>
								<span class="h-2 w-2 rounded-full bg-yellow-400"></span>
								<span class="h-2 w-2 rounded-full bg-green-400"></span>
							</div>
							<div class="bg-gray-900 px-2 py-2 flex gap-1.5">
								<div class="w-8 shrink-0 flex flex-col gap-1">
									<div class="flex items-center gap-1 mb-1">
										<div class="h-3 w-3 rounded bg-purple-500"></div>
										<div class="h-1.5 w-8 rounded bg-gray-700"></div>
									</div>
									<div class="h-1.5 w-full rounded bg-gray-800"></div>
									<div class="h-1.5 w-full rounded bg-gray-800"></div>
								</div>
								<div class="flex-1 flex flex-col gap-1">
									<div class="h-1.5 w-full rounded bg-gray-700"></div>
									<div class="h-1.5 w-3/4 rounded bg-gray-800"></div>
								</div>
							</div>
						</div>
						<div class="flex items-center gap-1.5 w-full px-0.5">
							<span class="text-xs text-ink-gray-7 font-medium flex-1 text-left"
								>Dark</span
							>
							<div
								:class="[
									'h-3.5 w-3.5 rounded-full border-2 flex items-center justify-center transition-colors',
									selectedTheme === 'dark'
										? 'border-blue-500 bg-blue-500'
										: 'border-outline-gray-3 bg-white',
								]"
							>
								<div
									v-if="selectedTheme === 'dark'"
									class="h-1.5 w-1.5 rounded-full bg-white"
								></div>
							</div>
						</div>
					</button>

					<!-- System -->
					<button
						class="flex flex-col items-start gap-1.5 cursor-pointer group"
						@click="selectedTheme = 'system'"
					>
						<div
							:class="[
								'w-40 rounded-lg border-2 overflow-hidden transition-colors',
								selectedTheme === 'system'
									? 'border-blue-500'
									: 'border-outline-gray-2 group-hover:border-outline-gray-3',
							]"
						>
							<!-- Half light half dark -->
							<div class="flex">
								<div class="w-1/2 bg-gray-100 px-1.5 py-1.5 flex gap-0.5">
									<span class="h-1.5 w-1.5 rounded-full bg-red-400"></span>
								</div>
								<div
									class="w-1/2 bg-gray-800 px-1.5 py-1.5 flex justify-end gap-0.5"
								>
									<span class="h-1.5 w-1.5 rounded-full bg-green-400"></span>
								</div>
							</div>
							<div class="flex">
								<div class="w-1/2 bg-white px-1.5 py-2 flex flex-col gap-1">
									<div class="h-1.5 w-full rounded bg-gray-200"></div>
									<div class="h-1.5 w-3/4 rounded bg-gray-100"></div>
									<div class="h-1.5 w-full rounded bg-gray-100"></div>
									<div class="h-1.5 w-3/4 rounded bg-gray-100"></div>
								</div>
								<div class="w-1/2 bg-gray-900 px-1.5 py-2 flex flex-col gap-1">
									<div class="h-1.5 w-full rounded bg-gray-700"></div>
									<div class="h-1.5 w-3/4 rounded bg-gray-800"></div>
									<div class="h-1.5 w-full rounded bg-gray-800"></div>
									<div class="h-1.5 w-3/4 rounded bg-gray-800"></div>
								</div>
							</div>
						</div>
						<div class="flex items-center gap-1.5 w-full px-0.5">
							<span class="text-xs text-ink-gray-7 font-medium flex-1 text-left"
								>System</span
							>
							<div
								:class="[
									'h-3.5 w-3.5 rounded-full border-2 flex items-center justify-center transition-colors',
									selectedTheme === 'system'
										? 'border-blue-500 bg-blue-500'
										: 'border-outline-gray-3 bg-white',
								]"
							>
								<div
									v-if="selectedTheme === 'system'"
									class="h-1.5 w-1.5 rounded-full bg-white"
								></div>
							</div>
						</div>
					</button>
				</div>
			</div>
		</section>

		<hr class="mb-8 border-outline-gray-2" />

		<!-- Device & Activity -->
		<section class="mb-8">
			<h2 class="mb-4 text-base font-semibold text-ink-gray-9">Device &amp; Activity</h2>

			<div v-if="devices.length" class="flex flex-col gap-0">
				<div
					v-for="device in devices"
					:key="device.id"
					class="flex items-center gap-3 border-b border-outline-gray-1 py-3.5 last:border-b-0"
				>
					<MonitorIcon class="h-4 w-4 text-ink-gray-4 shrink-0" />
					<div class="flex-1 min-w-0">
						<div class="flex items-center gap-2 flex-wrap">
							<p class="text-sm font-medium text-ink-gray-9">
								{{ device.browser
								}}<span v-if="device.os" class="font-normal text-ink-gray-5"
									>, {{ device.os }}</span
								>
							</p>
							<span
								v-if="device.isCurrent"
								class="inline-flex items-center rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20"
							>
								This Device
							</span>
						</div>
						<p class="text-xs text-ink-gray-5 mt-0.5">{{ device.location }}</p>
					</div>
					<Button variant="outline" size="sm" @click="signOutDevice(device.id)">
						<template #prefix>
							<LogOutIcon class="h-3.5 w-3.5" />
						</template>
						Sign out
					</Button>
				</div>
			</div>

			<div
				v-else
				class="flex flex-col items-center justify-center rounded-lg border border-dashed border-outline-gray-3 py-8 text-ink-gray-4"
			>
				<p class="text-sm">No active sessions.</p>
			</div>

			<button
				v-if="devices.length > 1"
				class="mt-3 flex items-center gap-1 text-sm text-ink-gray-6 hover:text-ink-gray-8 transition-colors"
				@click="signOutAll"
			>
				Sign out on all the device
				<ChevronRightIcon class="h-3.5 w-3.5" />
			</button>
		</section>

		<hr class="mb-8 border-outline-gray-2" />

		<!-- Danger Zone -->
		<section class="mb-8">
			<h2 class="mb-4 text-base font-semibold text-ink-gray-9">Danger Zone</h2>

			<div class="flex items-center justify-between py-2">
				<div>
					<p class="text-sm font-medium text-ink-gray-9">Delete account</p>
					<p class="text-xs text-ink-gray-5 mt-0.5">
						Permanently remove your account and all associated data.
					</p>
				</div>
				<Button variant="subtle" theme="red">
					<template #prefix>
						<AlertTriangleIcon class="h-3.5 w-3.5" />
					</template>
					Delete account
				</Button>
			</div>
		</section>
	</div>
</template>
